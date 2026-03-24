import numpy as np
import matplotlib.pyplot as plt
import cv2
import os


def preview_frame(cam1_file_list, cam2_file_list, frame_ind, cam1_min_max_x, cam1_min_max_y, cam2_min_max_x, cam2_min_max_y, cam1_rows, cam1_cols, cam2_rows, cam2_cols):
    # Camera 1
    ref_im = cv2.imread(cam1_file_list[frame_ind], cv2.IMREAD_UNCHANGED)
    
    plt.figure(figsize=(14, 4))
    plt.subplot(141)
    vmin, vmax = np.percentile(ref_im[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1], 0], (1, 99))
    plt.imshow(ref_im[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1], 0], vmin=vmin, vmax=vmax, cmap='gray')
    for x in cam1_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam1_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.title('Red')
    plt.subplot(142)
    vmin, vmax = np.percentile(ref_im[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1], 1], (1, 99))
    plt.imshow(ref_im[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1], 1], vmin=vmin, vmax=vmax, cmap='gray')
    for x in cam1_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam1_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.title('Green')
    plt.subplot(143)
    vmin, vmax = np.percentile(ref_im[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1], 2], (1, 99))
    plt.imshow(ref_im[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1], 2], vmin=vmin, vmax=vmax, cmap='gray')
    for x in cam1_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam1_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.title('Blue')
    plt.subplot(144)
    ref_gray = cv2.imread(cam1_file_list[frame_ind], cv2.IMREAD_GRAYSCALE)
    vmin, vmax = np.percentile(ref_gray[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1]], (1, 99))
    plt.imshow(ref_gray[cam1_min_max_y[0]:cam1_min_max_y[1], cam1_min_max_x[0]:cam1_min_max_x[1]], vmin=vmin, vmax=vmax, cmap='jet')
    for x in cam1_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam1_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.colorbar()
    plt.title('Gray')
    plt.suptitle(os.path.basename(cam1_file_list[frame_ind]))
    plt.tight_layout();
    
    # Camera 2
    ref_im = cv2.imread(cam2_file_list[frame_ind], cv2.IMREAD_UNCHANGED)
        
    plt.figure(figsize=(14, 4))
    plt.subplot(141)
    vmin, vmax = np.percentile(ref_im[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1], 0], (1, 99))
    plt.imshow(ref_im[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1], 0], vmin=vmin, vmax=vmax, cmap='gray')
    for x in cam2_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam2_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.title('Red')
    plt.subplot(142)
    vmin, vmax = np.percentile(ref_im[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1], 1], (1, 99))
    plt.imshow(ref_im[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1], 1], vmin=vmin, vmax=vmax, cmap='gray')
    for x in cam2_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam2_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.title('Green')
    plt.subplot(143)
    vmin, vmax = np.percentile(ref_im[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1], 2], (1, 99))
    plt.imshow(ref_im[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1], 2], vmin=vmin, vmax=vmax, cmap='gray')
    for x in cam2_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam2_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.title('Blue')
    plt.subplot(144)
    ref_gray = cv2.imread(cam2_file_list[frame_ind], cv2.IMREAD_GRAYSCALE)
    vmin, vmax = np.percentile(ref_gray[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1]], (1, 99))
    plt.imshow(ref_gray[cam2_min_max_y[0]:cam2_min_max_y[1], cam2_min_max_x[0]:cam2_min_max_x[1]], vmin=vmin, vmax=vmax, cmap='jet')
    for x in cam2_cols:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.5)
    for y in cam2_rows:
        plt.axhline(y=y, color='red', linestyle='--', linewidth=0.5)
    plt.colorbar()
    plt.title('Gray')
    plt.suptitle(os.path.basename(cam2_file_list[frame_ind]))
    plt.tight_layout();