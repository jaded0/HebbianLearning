import torch
import torch.nn as nn
import torch.nn.functional as F

from neurolab import params as P
from neurolab import utils
from neurolab.model import Model
import params as PP


class Net(Model):
	# Layer names
	CONV1 = 'conv1'
	RELU1 = 'relu1'
	POOL1 = 'pool1'
	BN1 = 'bn1'
	CONV2 = 'conv2'
	RELU2 = 'relu2'
	BN2 = 'bn2'
	CONV3 = 'conv3'
	RELU3 = 'relu3'
	POOL3 = 'pool3'
	BN3 = 'bn3'
	CONV4 = 'conv4'
	RELU4 = 'relu4'
	BN4 = 'bn4'
	CONV_OUTPUT = BN4 # Symbolic name for the last convolutional layer providing extracted features
	FLAT = 'flat'
	FC5 = 'fc5'
	RELU5 = 'relu5'
	BN5 = 'bn5'
	FC6 = 'fc6'
	Z = 'z'
	CLASS_SCORES = 'class_scores' # Name of the classification output providing the class scores
	VAE_OUTPUT = 'vae_output' # Name of the vae output consisting of reconstruction and latent variables statistics
	POOL_INDICES = 'pool_indices' # Name of the dictionary entry containing indices resulting from max pooling
	
	def __init__(self, config, input_shape=None):
		super(Net, self).__init__(config, input_shape)
		
		self.NUM_CLASSES = P.GLB_PARAMS[P.KEY_DATASET_METADATA][P.KEY_DS_NUM_CLASSES]
		self.DROPOUT_P = config.CONFIG_OPTIONS.get(P.KEY_DROPOUT_P, 0.5)
		self.NUM_LATENT_VARS = config.CONFIG_OPTIONS.get(PP.KEY_VAE_NUM_LATENT_VARS, 256)
		
		# Here we define the layers of our network
		
		# First convolutional layer
		self.conv1 = nn.Conv2d(3, 96, 5) # 3 input channels, 96 output channels, 5x5 convolutions
		self.bn1 = nn.BatchNorm2d(96) # Batch Norm layer
		# Second convolutional layer
		self.conv2 = nn.Conv2d(96, 128, 3) # 96 input channels, 128 output channels, 3x3 convolutions
		self.bn2 = nn.BatchNorm2d(128) # Batch Norm layer
		# Third convolutional layer
		self.conv3 = nn.Conv2d(128, 192, 3)  # 128 input channels, 192 output channels, 3x3 convolutions
		self.bn3 = nn.BatchNorm2d(192) # Batch Norm layer
		# Fourth convolutional layer
		self.conv4 = nn.Conv2d(192, 256, 3)  # 192 input channels, 256 output channels, 3x3 convolutions
		self.bn4 = nn.BatchNorm2d(256) # Batch Norm layer
		
		self.CONV_OUTPUT_SHAPE = utils.tens2shape(self.get_dummy_fmap()[self.CONV_OUTPUT])
		self.CONV_OUTPUT_SIZE = utils.shape2size(self.CONV_OUTPUT_SHAPE)
		
		# FC Layers
		self.fc5 = nn.Linear(self.CONV_OUTPUT_SIZE, 4096) # conv_output_size-dimensional input, 4096-dimensional output
		self.bn5 = nn.BatchNorm1d(4096) # Batch Norm layer
		self.fc6 = nn.Linear(4096, self.NUM_CLASSES) # 4096-dimensional input, NUM_CLASSES-dimensional output (one per class)
		self.fc_mu =  nn.Linear(4096, self.NUM_LATENT_VARS)  # 4096-dimensional input, NUM_LATENT_VARS-dimensional output
		self.fc_var =  nn.Linear(4096, self.NUM_LATENT_VARS)  # 4096-dimensional input, NUM_LATENT_VARS-dimensional output
		
		# Decoding Layers
		self.dec_fc0 = nn.Linear(self.NUM_LATENT_VARS, 4096)  # NUM_LATENT_VARS-dimensional input, 4096-dimensional output
		self.dec_bn0 = nn.BatchNorm1d(4096)  # Batch Norm layer
		self.dec_fc1 = nn.Linear(4096, self.CONV_OUTPUT_SIZE)  # 4096-dimensional input, CONV_OUTPUT_SIZE-dimensional output
		self.dec_bn1 = nn.BatchNorm1d(self.CONV_OUTPUT_SIZE)  # Batch Norm layer
		self.dec_conv2 = nn.ConvTranspose2d(256, 192, 3) # 256 input channels, 192 output channels, 3x3 transpose convolutions
		self.dec_bn2 = nn.BatchNorm2d(192) # Batch Norm layer
		self.dec_conv3 = nn.ConvTranspose2d(192, 128, 3) # 192 input channels, 128 output channels, 3x3 transpose convolutions
		self.dec_bn3 = nn.BatchNorm2d(128) # Batch Norm layer
		self.dec_conv4 = nn.ConvTranspose2d(128, 96, 3) # 128 input channels, 96 output channels, 3x3 transpose convolutions
		self.dec_bn4 = nn.BatchNorm2d(96) # Batch Norm layer
		self.dec_conv5 = nn.ConvTranspose2d(96, 3, 5) # 96 input channels, 3 output channels, 5x5 transpose convolutions
		self.dec_bn5 = nn.BatchNorm2d(3) # Batch Norm layer
	
	def get_conv_output(self, x):
		# Layer 1: Convolutional + ReLU activations + 2x2 Max Pooling + Batch Norm
		conv1_out = self.conv1(x)
		relu1_out = F.relu(conv1_out)
		pool1_out, pool1_indices = F.max_pool2d(relu1_out, 2, return_indices=True)
		bn1_out = self.bn1(pool1_out)
		
		# Layer 2: Convolutional + ReLU activations + Batch Norm
		conv2_out = self.conv2(bn1_out)
		relu2_out = F.relu(conv2_out)
		bn2_out = self.bn2(relu2_out)
		
		# Layer 3: Convolutional + ReLU activations + 2x2 Max Pooling + Batch Norm
		conv3_out = self.conv3(bn2_out)
		relu3_out = F.relu(conv3_out)
		pool3_out, pool3_indices = F.max_pool2d(relu3_out, 2, return_indices=True)
		bn3_out = self.bn3(pool3_out)
		
		# Layer 4: Convolutional + ReLU activations + Batch Norm
		conv4_out = self.conv4(bn3_out)
		relu4_out = F.relu(conv4_out)
		bn4_out = self.bn4(relu4_out)

		# Build dictionary containing outputs of each layer
		conv_out = {
			self.CONV1: conv1_out,
			self.RELU1: relu1_out,
			self.POOL1: pool1_out,
			self.BN1: bn1_out,
			self.CONV2: conv2_out,
			self.RELU2: relu2_out,
			self.BN2: bn2_out,
			self.CONV3: conv3_out,
			self.RELU3: relu3_out,
			self.POOL3: pool3_out,
			self.BN3: bn3_out,
			self.CONV4: conv4_out,
			self.RELU4: relu4_out,
			self.BN4: bn4_out,
			self.POOL_INDICES: {
				self.POOL1: pool1_indices,
				self.POOL3: pool3_indices
			}
		}
		return conv_out
	
	# Here we define the flow of information through the network
	def forward(self, x):
		# Compute the output feature map from the convolutional layers
		out = self.get_conv_output(x)
		pool_indices = out[self.POOL_INDICES]
		
		# Stretch out the feature map before feeding it to the FC layers
		flat = out[self.CONV_OUTPUT].view(-1, self.CONV_OUTPUT_SIZE)
		
		# Fifth Layer: FC with ReLU activations + Batch Norm
		fc5_out = self.fc5(flat)
		relu5_out = F.relu(fc5_out)
		bn5_out = self.bn5(relu5_out)
		
		# Sixth Layer: dropout + FC, outputs are the class scores
		fc6_out = self.fc6(F.dropout(bn5_out, p=self.DROPOUT_P, training=self.training))
		
		# Sampling
		mu = self.fc_mu(bn5_out)
		log_var = self.fc_var(bn5_out)
		std = torch.exp(0.5 * log_var)
		eps = torch.randn_like(std)
		z =  eps * std + mu
		
		# Decoding layers: double FC + transpose convolutions + Batch Norm
		dec_fc0_out = self.dec_fc0(z)
		dec_relu0_out = F.relu(dec_fc0_out)
		dec_bn0_out = self.dec_bn0(dec_relu0_out)
		dec_fc1_out = self.dec_fc1(dec_bn0_out)
		dec_relu1_out = F.relu(dec_fc1_out)
		dec_bn1_out = self.dec_bn1(dec_relu1_out)
		dec_conv2_out = self.dec_conv2(dec_bn1_out.view(-1, *self.CONV_OUTPUT_SHAPE))
		dec_relu2_out = F.relu(dec_conv2_out)
		dec_pool2_out = F.max_unpool2d(dec_relu2_out, pool_indices[self.POOL3], 2)
		dec_bn2_out = self.dec_bn2(dec_pool2_out)
		dec_conv3_out = self.dec_conv3(dec_bn2_out)
		dec_relu3_out = F.relu(dec_conv3_out)
		dec_bn3_out = self.dec_bn3(dec_relu3_out)
		dec_conv4_out = self.dec_conv4(dec_bn3_out)
		dec_relu4_out = F.relu(dec_conv4_out)
		dec_pool4_out = F.max_unpool2d(dec_relu4_out, pool_indices[self.POOL1], 2)
		dec_bn4_out = self.dec_bn4(dec_pool4_out)
		dec_conv5_out = self.dec_conv5(dec_bn4_out)
		dec_bn5_out = self.dec_bn5(dec_conv5_out)
		
		# Build dictionary containing outputs from convolutional and FC layers
		out[self.FLAT] = flat
		out[self.FC5] = fc5_out
		out[self.RELU5] = relu5_out
		out[self.BN5] = bn5_out
		out[self.FC6] = fc6_out
		out[self.Z] = z
		out[self.VAE_OUTPUT] = {
			P.KEY_CLASS_SCORES: fc6_out,
			P.KEY_AUTOENC_RECONSTR: dec_bn5_out,
			P.KEY_ELBO_MU: mu,
			P.KEY_ELBO_LOG_VAR: log_var,
		}
		out[self.CLASS_SCORES] = {P.KEY_CLASS_SCORES: fc6_out}
		return out
