import cv2
import numpy as np



def calculate_ssim(original, stego):
    """
    Calculate SSIM between original and stego RGB images.

    Returns:
        float
    """

    score = ssim(
        original,
        stego,
        channel_axis=2,
        data_range=255
    )

    return float(score)

class Metrics:
    def __init__(self):
        pass

    def mse(self, original, stego):
        error = np.mean((original.astype(np.float64) - stego.astype(np.float64)) ** 2)
        return error
    
    def psnr(self, original, stego):
        mse = self.mse(original, stego)

        if mse == 0:
            return float('inf')
        
        return 10 * np.log10((255 ** 2) / mse)
    
    def entropy(self, image):
        pixels = image.flatten()

        histogram = np.bincount(pixels, minlength=256)

        probability = histogram / np.sum(histogram)

        probability = probability[probability>0]

        return -np.sum(probability * np.log2(probability))
    
    def npcr(self, original, stego):
        if original.shape != stego.shape:
            raise ValueError("Images must have the same dimensions")

        # Count a pixel as changed if ANY channel changed
        changed_pixels = np.sum(np.any(original != stego, axis=2))

        total_pixels = original.shape[0] * original.shape[1]

        return (changed_pixels / total_pixels) * 100

    def ssim(self, original, stego):
        """
        SSIM implementation exactly as given in the paper.
        (Actually computes the Pearson Correlation Coefficient.)
        """

        if original.shape != stego.shape:
            raise ValueError("Images must have the same dimensions")

        original = original.astype(np.float64)
        stego = stego.astype(np.float64)

        scores = []

        # Compute separately for each RGB channel
        for c in range(original.shape[2]):

            A = original[:, :, c]
            B = stego[:, :, c]

            A_mean = np.mean(A)
            B_mean = np.mean(B)

            numerator = np.sum((A - A_mean) * (B - B_mean))

            denominator = np.sqrt(
                np.sum((A - A_mean) ** 2) *
                np.sum((B - B_mean) ** 2)
            )

            if denominator == 0:
                score = 1.0
            else:
                score = numerator / denominator

            scores.append(score)

        return np.mean(scores)

    def q_index(self, original, stego):
        """
        Universal Image Quality Index (Q-index)
        according to Equation (6) in the paper.
        """

        if original.shape != stego.shape:
            raise ValueError("Images must have the same dimensions")

        original = original.astype(np.float64)
        stego = stego.astype(np.float64)

        q_scores = []

        for c in range(original.shape[2]):

            x = original[:, :, c]
            y = stego[:, :, c]

            mean_x = np.mean(x)
            mean_y = np.mean(y)

            var_x = np.var(x)
            var_y = np.var(y)

            covariance = np.mean((x - mean_x) * (y - mean_y))

            numerator = 4 * covariance * mean_x * mean_y

            denominator = (
                (var_x + var_y) *
                (mean_x**2 + mean_y**2)
            )

            if denominator == 0:
                q = 1.0
            else:
                q = numerator / denominator

            q_scores.append(q)

        return np.mean(q_scores)