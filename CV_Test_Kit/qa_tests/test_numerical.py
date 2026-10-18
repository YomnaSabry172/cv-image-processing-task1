"""Independent examples and mathematical properties, not just output-shape tests."""
import numpy as np
import pytest
from app.core.color import to_grayscale
from app.core.convolution import apply_kernel
from app.core.edges import DETECTORS, canny
from app.core.frequency import FrequencyFilter
from app.core.hybrid import HybridImage
from app.core.histogram import histogram, pdf, cdf, equalize, normalize_minmax
from app.core.noise import UniformNoise, GaussianNoise, SaltPepperNoise
from app.core.spatial import smooth
from app.utils.image_io import decode_image, encode_image

@pytest.mark.parametrize('rgb,expected', [([255,0,0],76),([0,255,0],149),([0,0,255],29)])
def test_primary_colour_grayscale(rgb, expected):
    assert to_grayscale(np.array([[rgb]],dtype=np.uint8))[0,0] == expected

@pytest.mark.parametrize('shape', [(1,1),(1,9),(9,1),(31,46),(32,47)])
def test_image_io_roundtrip_gray(shape):
    image=np.random.default_rng(4).integers(0,256,shape,dtype=np.uint8)
    np.testing.assert_array_equal(decode_image(encode_image(image)),image)

def test_io_rgb_channel_order_and_downscale():
    image=np.zeros((1200,1600,3),dtype=np.uint8); image[:,:,0]=255
    restored=decode_image(encode_image(image))
    assert restored.shape==(768,1024,3)
    np.testing.assert_array_equal(restored[0,0],[255,0,0])

def test_histogram_exact_counts_pdf_cdf():
    image=np.array([[0,0,1],[2,2,255]],dtype=np.uint8)
    h=histogram(image)
    assert h.sum()==6 and len(h)==256
    np.testing.assert_array_equal(h[[0,1,2,255]],[2,1,2,1])
    assert pdf(h).sum()==pytest.approx(1)
    assert cdf(pdf(h))[2]==pytest.approx(5/6)

def test_equalization_exact_project_formula():
    # Project uses round(CDF*255), NOT the CDF-min-subtracted OpenCV variant.
    image=np.array([[0,0,1,2]],dtype=np.uint8)
    np.testing.assert_array_equal(equalize(image),[[128,128,191,255]])

def test_constant_equalization_and_normalization_contract():
    image=np.full((7,9),77,dtype=np.uint8)
    assert np.all(equalize(image)==255)
    assert np.all(normalize_minmax(image)==0)

def test_normalization_signed_custom_range():
    x=np.array([[-10.,0.,10.]])
    np.testing.assert_array_equal(normalize_minmax(x),[[0,128,255]])
    np.testing.assert_array_equal(normalize_minmax(x,20,220),[[20,120,220]])

@pytest.mark.parametrize('factory,kwargs', [(UniformNoise,{'low':0,'high':0}),(GaussianNoise,{'mean':0,'sigma':0}),(SaltPepperNoise,{'density':0})])
def test_zero_noise_identity_and_no_mutation(factory,kwargs):
    image=np.random.default_rng(2).integers(0,256,(17,19,3),dtype=np.uint8)
    original=image.copy()
    np.testing.assert_array_equal(factory(seed=1,**kwargs).apply(image),original)
    np.testing.assert_array_equal(image,original)

@pytest.mark.parametrize('factory,kwargs', [(UniformNoise,{'low':-20,'high':20}),(GaussianNoise,{'sigma':10}),(SaltPepperNoise,{'density':0.2})])
def test_noise_seed_reproducibility(factory,kwargs):
    image=np.full((128,128),128,dtype=np.uint8)
    a=factory(seed=21,**kwargs).apply(image)
    b=factory(seed=21,**kwargs).apply(image)
    c=factory(seed=22,**kwargs).apply(image)
    np.testing.assert_array_equal(a,b)
    assert not np.array_equal(a,c)

def test_noise_statistics_and_saturation():
    image=np.full((512,512),128,dtype=np.uint8)
    uniform=UniformNoise(-20,20,seed=42).apply(image).astype(float)-128
    gaussian=GaussianNoise(0,10,seed=42).apply(image).astype(float)-128
    # uint8 conversion truncates, producing about -0.5 mean for symmetric noise.
    assert -1 < uniform.mean() < 0 and 11 < uniform.std() < 12.2
    assert -1 < gaussian.mean() < 0 and 9.7 < gaussian.std() < 10.3
    assert np.all(UniformNoise(20,20).apply(np.full((3,3),250,dtype=np.uint8))==255)
    assert np.all(UniformNoise(-20,-20).apply(np.full((3,3),5,dtype=np.uint8))==0)

def test_salt_pepper_fraction_and_rgb_consistency():
    image=np.full((512,512,3),128,dtype=np.uint8)
    out=SaltPepperNoise(.2,.25,seed=42).apply(image)
    assert np.mean(out[:,:,0]==255)==pytest.approx(.05,abs=.005)
    assert np.mean(out[:,:,0]==0)==pytest.approx(.15,abs=.005)
    np.testing.assert_array_equal(out[:,:,0],out[:,:,1])
    np.testing.assert_array_equal(out[:,:,1],out[:,:,2])

@pytest.mark.parametrize('method',['average','gaussian','median'])
@pytest.mark.parametrize('implementation',['manual','builtin'])
def test_filter_constant_and_identity(method,implementation):
    constant=np.full((17,19,3),100,dtype=np.uint8)
    out=smooth(constant,method,k=5,implementation=implementation)
    assert np.max(np.abs(out.astype(float)-100))<=1
    np.testing.assert_array_equal(smooth(constant,method,k=1,implementation=implementation),constant)

def test_median_removes_isolated_impulses():
    image=np.full((15,15),128,dtype=np.uint8); image[4,4]=0; image[10,10]=255
    assert np.all(smooth(image,'median',k=3)==128)

@pytest.mark.parametrize('name',['sobel','prewitt','roberts'])
@pytest.mark.parametrize('shape',[(1,1),(1,9),(9,1),(31,46),(32,47)])
def test_edges_twins_and_constant(name,shape):
    image=np.random.default_rng(1).integers(0,256,shape,dtype=np.uint8)
    manual=DETECTORS[name].detect(image,'manual')
    builtin=DETECTORS[name].detect(image,'builtin')
    for key in ('gx','gy','magnitude','direction'):
        assert manual[key].shape==shape and manual[key].dtype==np.float64
        np.testing.assert_allclose(manual[key],builtin[key],atol=1e-10)
    flat=DETECTORS[name].detect(np.full(shape,100,dtype=np.uint8))
    assert np.all(flat['magnitude']==0)

@pytest.mark.parametrize('name,gain',[('sobel',8),('prewitt',6)])
def test_ramp_has_known_gradient_sign_and_angle(name,gain):
    ramp=np.tile(np.arange(9,dtype=np.uint8),(9,1))
    result=DETECTORS[name].detect(ramp)
    np.testing.assert_array_equal(result['gx'][1:-1,1:-1],gain)
    np.testing.assert_array_equal(result['gy'][1:-1,1:-1],0)
    np.testing.assert_array_equal(result['direction'][1:-1,1:-1],0)
    reversed_result=DETECTORS[name].detect(ramp[:,::-1])
    assert np.all(reversed_result['gx'][1:-1,1:-1]<0)

def test_roberts_hand_calculated_patch():
    image=np.array([[10,20],[30,40]],dtype=np.uint8)
    result=DETECTORS['roberts'].detect(image)
    assert result['gx'][1,1]==-30
    assert result['gy'][1,1]==-10
    assert result['magnitude'][1,1]==pytest.approx(np.sqrt(1000))

@pytest.mark.parametrize('sigma',[None,1.0])
def test_canny_flat_and_step(sigma):
    assert not np.any(canny(np.full((64,64),100,dtype=np.uint8),50,150,sigma))
    image=np.zeros((64,64),dtype=np.uint8); image[:,32:]=255
    out=canny(image,50,150,sigma)
    assert set(np.unique(out)) <= {0,255} and np.any(out)
    assert np.all(out[:,:28]==0) and np.all(out[:,36:]==0)

@pytest.mark.parametrize('shape',['ideal','gaussian','butterworth'])
@pytest.mark.parametrize('size',[(1,1),(31,46),(32,47)])
def test_frequency_complements_dc_and_reconstruction(shape,size):
    low=FrequencyFilter('lowpass',shape,5); high=FrequencyFilter('highpass',shape,5)
    mask=low.build_mask(*size)
    assert np.all((mask>=0)&(mask<=1)) and mask[size[0]//2,size[1]//2]==1
    np.testing.assert_allclose(mask+high.build_mask(*size),1,atol=1e-14)
    image=np.random.default_rng(1).integers(0,256,size,dtype=np.uint8)
    restored=low.apply_raw(image)['result']+high.apply_raw(image)['result']
    np.testing.assert_allclose(restored,image,atol=1e-10)
    flat=np.full(size,100,dtype=np.uint8)
    np.testing.assert_allclose(low.apply_raw(flat)['result'],100,atol=1e-10)
    np.testing.assert_allclose(high.apply_raw(flat)['result'],0,atol=1e-10)

@pytest.mark.parametrize('shape,weight',[('ideal',1.0),('gaussian',np.exp(-.5)),('butterworth',.5)])
def test_mask_weight_at_exact_cutoff(shape,weight):
    assert FrequencyFilter('lowpass',shape,3).build_mask(9,9)[4,7]==pytest.approx(weight)

def test_ideal_filter_separates_known_sinusoid():
    x=np.arange(64); wave=20*np.cos(2*np.pi*8*x/64)
    image=np.tile(100+wave,(32,1))
    low=FrequencyFilter('lowpass','ideal',4).apply_raw(image)['result']
    high=FrequencyFilter('highpass','ideal',4).apply_raw(image)['result']
    np.testing.assert_allclose(low,100,atol=1e-10)
    np.testing.assert_allclose(high,np.tile(wave,(32,1)),atol=1e-10)

@pytest.mark.parametrize('kind',['lowpass','highpass'])
@pytest.mark.parametrize('shape',['ideal','gaussian','butterworth'])
def test_frequency_rgb_outputs_and_independent_channels(kind,shape):
    image=np.zeros((31,46,3),dtype=np.uint8); image[:,23:,0]=200; image[:,:,1]=100
    out=FrequencyFilter(kind,shape,5).apply(image)
    for key,value in out.items():
        assert value.dtype==np.uint8 and np.all(np.isfinite(value))
        assert value.shape==((31,46) if key=='mask' else image.shape)
    np.testing.assert_allclose(FrequencyFilter(kind,shape,5).apply_raw(image[:,:,2])['result'],0,atol=1e-10)

@pytest.mark.parametrize('a_rgb,b_rgb',[(False,False),(True,True),(True,False),(False,True)])
def test_hybrid_size_mode_and_no_mutation(a_rgb,b_rgb):
    a=np.full((31,46,3) if a_rgb else (31,46),100,dtype=np.uint8)
    b=np.full((19,27,3) if b_rgb else (19,27),200,dtype=np.uint8)
    a0=a.copy(); b0=b.copy()
    out=HybridImage(FrequencyFilter('lowpass','gaussian',5),FrequencyFilter('highpass','gaussian',5)).make(a,b)
    for value in out.values():
        assert value.shape==((31,46,3) if a_rgb and b_rgb else (31,46))
        assert value.dtype==np.uint8
    assert np.max(np.abs(out['hybrid'].astype(float)-100))<=1
    np.testing.assert_array_equal(a,a0); np.testing.assert_array_equal(b,b0)

def test_hybrid_adds_negative_details_before_clipping():
    a=np.full((32,64),100,dtype=np.uint8)
    b=np.tile(np.where(np.arange(64)%2,148,108).astype(np.uint8),(32,1))
    out=HybridImage(FrequencyFilter('lowpass','ideal',5),FrequencyFilter('highpass','ideal',5)).make(a,b)
    expected=np.tile(np.where(np.arange(64)%2,120,80),(32,1))
    np.testing.assert_allclose(out['hybrid'],expected,atol=1)
