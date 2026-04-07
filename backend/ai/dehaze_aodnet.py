import cv2

def dehaze_video_frame(frame):
    """
    Dehazing fallback utilizing Contrast Limited Adaptive Histogram Equalization (CLAHE).
    This acts as a high-speed, highly effective contrast enhancement tool for fog removal in realtime.
    Since full AOD-Net PyTorch weights dynamically require heavy external downloads, this simulates
    the rapid visibility improvement necessary for accurate YOLO detections in 30fps+ video.
    """
    try:
        # Convert the BGR frame to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        # Apply CLAHE to the L (Lightness) channel to neutralize fog masking
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l_channel)
        
        # Merge the enhanced L-channel with original A and B channels
        merged_lab = cv2.merge((cl, a_channel, b_channel))
        
        # Convert back to BGR color space
        dehazed_frame = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
        return dehazed_frame
    except Exception as e:
        print(f"Dehaze error: {e}")
        return frame
