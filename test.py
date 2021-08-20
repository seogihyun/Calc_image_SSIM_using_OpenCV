import cv2
import argparse
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os.path

def SSIM(roi_source, roi_target):
  roi_source = cv2.cvtColor(roi_source, cv2.COLOR_BGR2GRAY)
  roi_target = cv2.cvtColor(roi_target, cv2.COLOR_BGR2GRAY)
  score, diff = ssim(roi_source, roi_target, full=True) # full=True : 이미지 전체에 대해서 구조비교를 수행함.
  diff = (diff * 255).astype("uint8")
  return score, diff

def measurement_table(original, target):

  name, extension = os.path.basename(original).split('.')
  name2, extension2 = os.path.basename(target).split('.')

  
  try:
    cap = cv2.VideoCapture('./{title}.{extension}'.format(title=str(name), extension=str(extension)))
    cap2 = cv2.VideoCapture('./{title}.{extension}'.format(title=str(name2), extension=str(extension2)))
  
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')

    print(fps, width, height, fourcc)
    targte_name = '{name}_{title}.{extension}'.format(name='Gihyun', title=str(name), extension=str(extension))
    print(targte_name)
    out = cv2.VideoWriter(targte_name, fourcc, fps, (width//2*3, height))
  except:
    print('Try again!')
    return

  while True:

    """ 재생되는 비디오의 한 프레임씩 읽어옴 """
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    if ret and ret2:
      """ 원본에서 자르기를 원하는 부분 설정 """
      original_copy = frame[:, int(width*(1/4)):int(width*(3/4))]
      target_copy = frame2[:, int(width*(1/4)):int(width*(3/4))]

      """ SSIM 계산 """
      score, diff = SSIM(original_copy, target_copy)

      """ 이미지에 이름 추가 """
      original_name = '.mp4'
      target_name = '.ts'
      diff_name = 'SSIM Score : ' + str(round(score, 3))
      # org (글자 위치)
      org = (10, 50) 
      # font 
      font = cv2.FONT_HERSHEY_SIMPLEX  
      # fontScale (글자 크기)
      fontScale = 1
      # Blue color in BGR
      color = (0, 0, 0) 
      # Line thickness of 2 px (두께) 
      thickness = 2
      # Using cv2.putText() method  
      original_copy = cv2.putText(original_copy, original_name, org, font, fontScale, color, thickness, cv2.LINE_AA) 
      target_copy = cv2.putText(target_copy, target_name, org, font, fontScale, color, thickness, cv2.LINE_AA)
      diff = cv2.putText(diff, diff_name, org, font, fontScale, color, thickness, cv2.LINE_AA)

      img2 = np.zeros_like(target_copy)
      img2[:,:,0] = diff
      img2[:,:,1] = diff
      img2[:,:,2] = diff

      """ 이미지 합치기 """
      output = np.hstack((original_copy, target_copy, img2))

      print(f'SSIM Score: {round(score, 3)}')
      out.write(output)
    else:
      break

  out.release()
  cap.release()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--original_path', type=str, default='./origin.mp4')
  parser.add_argument('--target_path', type=str, default='./target1.ts')
  args = parser.parse_args()

  measurement_table(args.original_path, args.target_path)
