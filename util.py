import stft
from scipy.signal import hamming
import numpy as np
import tensorflow as tf

############################################################################
##  Spectrogram util functions
############################################################################

CONST = 10000  # prevent input values from being too large
setting = None

def create_spectrogram_from_audio(data):
	spectrogram = stft.spectrogram(data, framelength=512, window=hamming).transpose() / CONST
	setting = spectrogram.stft_settings  # setting is going to be same for all spectrograms
	spectrogram = np.asarray(spectrogram)
	
	# divide the real and imaginary components of each element 
	# concatenate the matrix with the real components and the matrix with imaginary components
	concatenated = np.concatenate([np.real(spectrogram), np.imag(spectrogram)], axis=1)
	concatenated = np.asarray(concatenated, dtype=np.float32)
	return concatenated

def create_audio_from_spectrogram(spec):
	return stft.ispectrogram(SpectrogramArray(spec, stft_settings=setting).transpose() * CONST)

############################################################################
##  Vector Product Functions
############################################################################

def tf_broadcast_matrix_mult(a, b):
	'''
	a is 3-d and b is 2-d
	'''
	orig_shape = a.get_shape().as_list()
	a_ = tf.reshape(a, [-1, orig_shape[-1]])
	mul = tf.matmul(a_, b)
	new_shape = orig_shape[:-1] + b.get_shape().as_list()[-1:]
	return tf.reshape(mul, new_shape)

def vector_product_matrix(X, W):
	return tf.transpose([tf_broadcast_matrix_mult(X[:,:,:,1], W[:,:,2]) - tf_broadcast_matrix_mult(X[:,:,:,2], W[:,:,1]),
		tf_broadcast_matrix_mult(X[:,:,:,2], W[:,:,0]) - tf_broadcast_matrix_mult(X[:,:,:,0], W[:,:,2]),
		tf_broadcast_matrix_mult(X[:,:,:,0], W[:,:,1]) - tf_broadcast_matrix_mult(X[:,:,:,1], W[:,:,0])], (1, 2, 3, 0))