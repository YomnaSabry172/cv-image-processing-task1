"""Create deterministic diagnostic fixtures, not AI-generated imagery."""
from pathlib import Path
import cv2
import numpy as np

out=Path(__file__).resolve().parent/'images'; out.mkdir(exist_ok=True)
def save(name,image):
    encoded=image[:,:,::-1] if image.ndim==3 and image.shape[2]==3 else image
    assert cv2.imwrite(str(out/name),encoded)

save('01_constant_128.png',np.full((256,256),128,dtype=np.uint8))
save('02_gray_ramp.png',np.tile(np.arange(256,dtype=np.uint8),(256,1)))
step=np.zeros((256,256),dtype=np.uint8); step[:,128:]=255
save('03_vertical_step.png',step); save('04_horizontal_step.png',step.T)
checker=((np.indices((256,256)).sum(axis=0)//1)%2*255).astype(np.uint8)
save('05_fine_checkerboard.png',checker)
patches=np.zeros((256,256,3),dtype=np.uint8)
patches[:128,:128]=[255,0,0]; patches[:128,128:]=[0,255,0]
patches[128:,:128]=[0,0,255]; patches[128:,128:]=[255,255,255]
save('06_rgb_patches.png',patches)
low=np.tile(np.rint(np.linspace(80,120,256)).astype(np.uint8),(256,1))
save('07_low_contrast.png',low)
rng=np.random.default_rng(42)
noisy=np.full((256,256),128,dtype=np.uint8); mask=rng.random(noisy.shape)
noisy[mask<.05]=0; noisy[(mask>=.05)&(mask<.1)]=255
save('08_salt_pepper_seed42.png',noisy)
odd=rng.integers(0,256,(31,46,3),dtype=np.uint8); save('09_odd_rgb_31x46.png',odd)
large=np.zeros((1200,1600,3),dtype=np.uint8); large[:,:,:]=[210,70,20]
save('10_large_rgb_1600x1200.png',large)
save('11_tiny_1x1.png',np.array([[128]],dtype=np.uint8))
save('12_thin_2048x1.png',np.full((1,2048),128,dtype=np.uint8))
save('13_primary_rgb.png',np.array([[[255,0,0],[0,255,0],[0,0,255]]],dtype=np.uint8))
save('14_hist_exact_4x1.png',np.array([[0,0,1,2]],dtype=np.uint8))
# Simple aligned geometric images for hybrid mechanics; use real aligned portraits for perception.
y,x=np.indices((256,256)); disk=(x-128)**2+(y-128)**2<75**2
broad=np.full((256,256),40,dtype=np.uint8); broad[disk]=200
fine=np.where((x//4)%2,180,80).astype(np.uint8)
save('15_hybrid_A_disk.png',broad); save('16_hybrid_B_stripes.png',fine)
save('17_step.jpg',step); save('18_rgb.bmp',patches); save('19_rgb.webp',patches)
(out/'20_invalid.txt').write_text('This is not an image.')
(out/'21_corrupt.png').write_bytes(b'not really a PNG')
print(f'Wrote 21 fixtures to {out}')
