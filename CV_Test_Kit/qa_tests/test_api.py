"""API success contracts, validation, image decoding, and a chained workflow."""
import base64
import numpy as np
import pytest
from app.utils.image_io import encode_image,decode_image

CASES=[
    ('grayscale',{}, {'result'}),
    *[('noise',{'type':kind,'seed':42},{'result'}) for kind in ('uniform','gaussian','salt_pepper')],
    *[('filter',{'method':method,'kernel_size':3,'implementation':impl}, {'manual','builtin','difference'} if impl=='compare' else {'result'}) for method in ('average','gaussian','median') for impl in ('manual','builtin','compare')],
    *[('edges',{'method':method,'implementation':impl},{'gx','gy','magnitude','direction'}) for method in ('sobel','prewitt','roberts') for impl in ('manual','builtin')],
    ('edges',{'method':'canny','low':50,'high':150},{'result'}),
    ('edges',{'method':'canny','low':50,'high':150,'blur_sigma':1},{'result'}),
    ('histogram',{},set()),('equalize',{}, {'result'}),('normalize',{}, {'result'}),
    *[('frequency',{'kind':kind,'shape':shape,'cutoff':5,'order':2},{'result','spectrum','mask','filtered_spectrum'}) for kind in ('lowpass','highpass') for shape in ('ideal','gaussian','butterworth')],
]

@pytest.fixture
def image_url():
    return encode_image(np.random.default_rng(5).integers(0,256,(31,46,3),dtype=np.uint8))

def test_health(client):
    response=client.get('/api/health')
    assert response.status_code==200 and response.json()=={'status':'ok'}

@pytest.mark.parametrize('colour',[False,True],ids=['gray','rgb'])
@pytest.mark.parametrize('endpoint,params,keys',CASES)
def test_all_success_contracts(client,colour,endpoint,params,keys):
    image=np.random.default_rng(6).integers(0,256,(31,46,3) if colour else (31,46),dtype=np.uint8)
    response=client.post('/api/'+endpoint,json={'image':encode_image(image),**params})
    assert response.status_code==200,response.text
    body=response.json()
    assert {'images','data','meta'}<=body.keys()
    assert set(body['images'])==keys
    assert isinstance(body['meta']['time_ms'],(int,float)) and body['meta']['time_ms']>=0
    for value in body['images'].values():
        restored=decode_image(value)
        assert restored.shape[:2]==image.shape[:2]
    if endpoint=='histogram':
        assert body['data']['mode']==('rgb' if colour else 'gray')
        for channel in body['data']['channels'].values():
            assert sum(channel['hist'])==31*46
            assert len(channel['hist'])==len(channel['pdf'])==len(channel['cdf'])==256
            assert channel['cdf'][-1]==pytest.approx(1)
    if endpoint=='filter' and params['implementation']=='compare':
        stats=body['data']
        assert stats['max_abs_diff']<=1
        assert stats['time_manual_ms']>=0 and stats['time_builtin_ms']>=0
        assert np.isfinite(stats['speedup']) and stats['speedup']>=0

@pytest.mark.parametrize('shape',['ideal','gaussian','butterworth'])
def test_hybrid_api(client,image_url,shape):
    b=encode_image(np.full((19,27),100,dtype=np.uint8))
    response=client.post('/api/hybrid',json={'image_a':image_url,'image_b':b,'shape':shape,'low_cutoff':5,'high_cutoff':5})
    assert response.status_code==200,response.text
    body=response.json()
    assert set(body['images'])=={'hybrid','low_component','high_component'}
    for value in body['images'].values():
        assert decode_image(value).shape==(31,46)

def test_noise_filter_chain_uses_actual_noisy_image(client):
    clean=np.full((64,64),128,dtype=np.uint8)
    noise=client.post('/api/noise',json={'image':encode_image(clean),'type':'salt_pepper','density':.1,'seed':42})
    assert noise.status_code==200
    noisy=noise.json()['images']['result']
    filtered=client.post('/api/filter',json={'image':noisy,'method':'median','kernel_size':3})
    assert filtered.status_code==200
    before=decode_image(noisy).astype(float)
    after=decode_image(filtered.json()['images']['result']).astype(float)
    assert np.mean((after-clean)**2)<np.mean((before-clean)**2)

@pytest.mark.parametrize('endpoint,params,_',CASES)
def test_corrupt_image_returns_400(client,endpoint,params,_):
    corrupt='data:image/png;base64,'+base64.b64encode(b'not an image').decode()
    response=client.post('/api/'+endpoint,json={'image':corrupt,**params})
    assert response.status_code==400,response.text
    assert response.json().get('detail')

# Acceptance tests: bugs remain visible instead of being marked as expected failures.
INVALID_CASES=[
    ('filter',{'method':'average','kernel_size':2}),
    ('filter',{'method':'unknown'}),
    ('filter',{'method':'gaussian','sigma':0}),
    ('filter',{'method':'gaussian','sigma':None}),
    ('filter',{'method':'average','implementation':'invalid'}),
    ('edges',{'method':'sobel','implementation':'invalid'}),
    ('edges',{'method':'unknown'}),
    ('edges',{'method':'canny','low':150,'high':50}),
    ('edges',{'method':'canny','blur_sigma':0}),
    ('noise',{'type':'uniform','low':20,'high':-20}),
    ('noise',{'type':'gaussian','sigma':-1}),
    ('noise',{'type':'salt_pepper','density':-0.1}),
    ('noise',{'type':'salt_pepper','salt_ratio':1.1}),
    ('frequency',{'cutoff':0}),
    ('frequency',{'order':0}),
    ('frequency',{'shape':'unknown'}),
]
@pytest.mark.parametrize('endpoint,params',INVALID_CASES)
def test_invalid_parameters_return_400(client,image_url,endpoint,params):
    response=client.post('/api/'+endpoint,json={'image':image_url,**params})
    assert response.status_code==400,f'{endpoint} {params}: got {response.status_code}, {response.text}'
    assert response.json().get('detail')

@pytest.mark.parametrize('image',['','data:image/png;base64,'])
def test_empty_image_rejected_without_server_error(client,image):
    response=client.post('/api/grayscale',json={'image':image})
    assert response.status_code==400,response.text

@pytest.mark.parametrize('endpoint',['grayscale','noise','filter','edges','frequency','histogram','equalize','normalize','hybrid'])
def test_missing_required_fields_return_validation_error(client,endpoint):
    response=client.post('/api/'+endpoint,json={})
    assert response.status_code==422,response.text

@pytest.mark.parametrize('shape',[(1,2048),(2048,1)])
def test_very_thin_large_images_remain_valid(client,shape):
    image=np.full(shape,100,dtype=np.uint8)
    response=client.post('/api/grayscale',json={'image':encode_image(image)})
    assert response.status_code==200,response.text
    decoded=decode_image(response.json()['images']['result'])
    assert min(decoded.shape)>=1 and max(decoded.shape)<=1024

def test_cors_preflight(client):
    response=client.options('/api/frequency',headers={'Origin':'http://localhost:5173','Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'content-type'})
    assert response.status_code==200
    assert response.headers.get('access-control-allow-origin')=='http://localhost:5173'
