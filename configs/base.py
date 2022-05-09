from neurolab import params as P
import params as PP


#   whiten    lrn    scale_in    offset_in    scale_out    out    scale_in    offset_in    scale_out    bn1    bn5
#   No        tanh   1.          0.           1.           tanh   1.          0.           1.           60     50
#   Yes       tanh   1.          0.           1.           tanh   1.          0.           1.           59     52
#   No        tanh   1.          0.           1.           sshr   1.          0.           1.           59     16
#   No        tanh   1.          0.           1.           sshr   .1          0.           1.           60     54
#   No        tanh   .1          0.           1.           sshr   .1          0.           1.           60     54
#   No        tanh   1.          0.           1.           sshr   .1          0.           .1           60     54
#   No        tanh   .1          0.           .1           sshr   .1          0.           .1           60     54
#   Yes       tanh   1.          0.           1.           sshr   .1          0.           1.           61     52
# ---------------------------------------------------------------------------------------------------------------
#   No        tanh   1.          0.           1.           relu   1.          0.           1.           62     54
#   Yes       tanh   1.          0.           1.           relu   1.          0.           1.           62     50
#   No        tanh   1.          0.           1.           relu   1.          .2           1.           62     57
#   No        tanh   1.          0.           1.           relu   1.          .4           1.           61     58
#   No        tanh   1.          0.           1.           relu   1.          .8           1.           59     57
#   No        tanh   1.          0.           1.           relu   1.          1.           1.           59     56
#   No        tanh   1.          0.           1.           relu   1.          2.           1.           58     55
#   No        tanh   1.          0.           1.           relu   1.         -.2           1.           61     47
#   Yes       tanh   1.          0.           1.           relu   1.          .4           1.           60     54
# ---------------------------------------------------------------------------------------------------------------
#   No        remp   1.          0.           1.           relu   1.          0.           1.           63     52
#   No        remp   1.          1.5          1.           relu   1.          0.           1.           63     50
#   No        remp   1.          1.5          1.           relu   1.          .5           1.           62     53
#   No        remp   1.          1.5          1.           relu   1.         -.5           1.           61     28
#   No        remp   1.          1.5          1.           relu   1.          1.           1.           61     51
#   No        remp   1.          1.5          1.           relu   1.          1.5          1.           60     52
#   No        remp   1.          1.5          1.           relu   1.          2.           1.           60     52
#   Yes       remp   1.          1.5          1.           relu   1.          .5           1.           60     50
#   No        shmp   1.          0.           1.           relu   1.          0.           1.           63     52
#   No        shmp   1.          .3           1.           relu   1.          0.           1.           63     51
#   No        shmp   1.          .3           1.           relu   1.          .1           1.           63     53
#   No        shmp   1.          .3           1.           relu   1.         -.1           1.           63     48
#   No        shmp   1.          .3           1.           relu   1.          .3           1.           63     55
#   No        shmp   1.          .3           1.           relu   1.          .6           1.           61     55
#   No        shmp   1.          .3           1.           relu   1.          1.           1.           60     55
#   No        shmp   1.          .3           1.           relu   1.          2.           1.           60     54
#   Yes       shmp   1.          .3           1.           relu   1.          .3           1.           60     50
# No modified bn
# Post-nonlinear demixers
# Squared elu out act and const--1/x lrn act for mi maximization, with gelu sq out act
# Adaptive nonlinearities
# Splitting nonlinearities
# PCA with splitting nonlinearities
# PCA with neurons with multiple different bias targets to achieve muiltiple splits
# Clustering with gauss nonlinearity integrated with vector projection similarity using weight vector as mean encoding and bias
#  for variance, so that it is possible to find aligned clusters with dot product-based similarity.

config_ica = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'models.hebb.model_6l.Net',
	P.KEY_NET_OUTPUTS: 'fc6',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None, #2,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
	P.KEY_LOCAL_LRN_RULE: 'ica', #'hpca', #'ica', #'hwta',
	#PP.KEY_WTA_COMPETITIVE_ACT: 'hebb.functional.esoftwta',
	#PP.KEY_WTA_K: .02,
	PP.KEY_LRN_ACT: 'hebb.functional.tanh',
	PP.KEY_LRN_ACT_SCALE_IN: 1e-3, #1.,
	PP.KEY_LRN_ACT_OFFSET_IN: 0.,
	PP.KEY_LRN_ACT_SCALE_OUT: 1.,
	PP.KEY_OUT_ACT: 'hebb.functional.sshrink', #tanh',
	PP.KEY_OUT_ACT_SCALE_IN: 1e-3, #1.,
	PP.KEY_OUT_ACT_OFFSET_IN: 0.,
	PP.KEY_OUT_ACT_SCALE_OUT: 1e-3, #1.,
}

config_hebb = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'models.hebb.model_6l.Net',
	P.KEY_NET_OUTPUTS: 'fc6',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None, #2,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
	P.KEY_LOCAL_LRN_RULE: 'hpca', #'ica', #'hwta',
	#PP.KEY_WTA_COMPETITIVE_ACT: 'hebb.functional.esoftwta',
	#PP.KEY_WTA_K: .02,
	PP.KEY_LRN_ACT: 'hebb.functional.relu',
	PP.KEY_OUT_ACT: 'hebb.functional.relu',
}

fc_on_hebb_layer = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'models.gdes.fc.Net',
	P.KEY_NET_OUTPUTS: 'fc',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None, #2,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20, #40,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
	P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
    P.KEY_LR_DECAY: 0.5, #0.1,
    P.KEY_MILESTONES: range(10, 20), #[20, 30],
    P.KEY_MOMENTUM: 0.9,
    P.KEY_L2_PENALTY: 5e-4,
	P.KEY_DROPOUT_P: 0.5,
	P.KEY_LOCAL_LRN_RULE: 'ica', #'hpca', #'hwta', #'ica',
	#PP.KEY_WTA_COMPETITIVE_ACT: 'hebb.functional.esoftwta',
	#PP.KEY_WTA_K: .02,
	PP.KEY_LRN_ACT: 'hebb.functional.tanh',
	PP.KEY_LRN_ACT_SCALE_IN: 1e-3, #1.,
	PP.KEY_LRN_ACT_OFFSET_IN: 0.,
	PP.KEY_LRN_ACT_SCALE_OUT: 1.,
	PP.KEY_OUT_ACT: 'hebb.functional.sshrink', #tanh',
	PP.KEY_OUT_ACT_SCALE_IN: 1e-3, #1.,
	PP.KEY_OUT_ACT_OFFSET_IN: 0.,
	PP.KEY_OUT_ACT_SCALE_OUT: 1e-3, #1.,
	P.KEY_PRE_NET_MODULES: ['models.hebb.model_6l.Net'],
	P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/base/config_hebb/iter' + P.STR_TOKEN + '/models/model0.pt'],
	P.KEY_PRE_NET_OUTPUTS: ['bn5'],
}

config_gdes = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'models.gdes.model_6l.Net',
	P.KEY_NET_OUTPUTS: 'fc6',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	#P.KEY_DA_ROT_DEGREES: 30,
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20, #40,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
	P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
    P.KEY_LR_DECAY: 0.5, # 0.1,
    P.KEY_MILESTONES: range(10, 20), # [20, 30],
    P.KEY_MOMENTUM: 0.9,
    P.KEY_L2_PENALTY: 5e-2,
	P.KEY_DROPOUT_P: 0.5,
	P.KEY_HPMANAGER: 'neurolab.hpsearch.DiscAltMinHPManager',
	P.KEY_HPSEARCH_PARAMS: {P.KEY_LEARNING_RATE: [1e-2, 1e-3, 1e-4], P.KEY_L2_PENALTY: [5e-2, 5e-3, 5e-4]},
}

fc_on_gdes_layer = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'models.gdes.fc.Net',
	P.KEY_NET_OUTPUTS: 'fc',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20, #40,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
	P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
    P.KEY_LR_DECAY: 0.5, #0.1,
    P.KEY_MILESTONES: range(10, 20), #[20, 30],
    P.KEY_MOMENTUM: 0.9,
    P.KEY_L2_PENALTY: 5e-4,
	P.KEY_DROPOUT_P: 0.5,
	P.KEY_PRE_NET_MODULES: ['models.gdes.model_2l.Net'],
	P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/base/config_gdes/iter' + P.STR_TOKEN + '/models/model0.pt'],
	P.KEY_PRE_NET_OUTPUTS: ['bn1'],
}

btmupexp_fc_on_gdes_layer = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.btmupexp.BtmUpExperiment',
	P.KEY_SUBCONFIG_LIST: ['configs.base.config_gdes', 'configs.base.fc_on_gdes_layer'],
	'exp0+exp1::' + P.KEY_NUM_EPOCHS: 2,
	'exp0+exp1::' + P.KEY_LEARNING_RATE: 1e-3,
	'exp0::' + P.KEY_L2_PENALTY: 5e-2,
	'exp1::' + P.KEY_L2_PENALTY: 5e-4,
	'exp1::' + P.KEY_PRE_NET_MDL_PATHS: ['exp0/iter' + P.STR_TOKEN + '/models/model0.pt'],
	P.KEY_HPMANAGER: 'neurolab.hpsearch.DiscAltMinHPManager',
	P.KEY_HPSEARCH_PARAMS: {'exp0+exp1::' + P.KEY_LEARNING_RATE: [1e-4, 1e-3], 'exp0::' + P.KEY_L2_PENALTY: [5e-2, 5e-3, 5e-4], 'exp1::' + P.KEY_L2_PENALTY: [5e-2, 5e-3, 5e-4]},
}

sk_on_gdes_layer = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'neurolab.model.skclassif.KNNClassifier',
	P.KEY_NET_OUTPUTS: 'clf',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 1, #2,
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
	P.KEY_SKCLF_NUM_SAMPLES: 40000, #80000,
	P.KEY_NYSTROEM_N_COMPONENTS: 1000,
	P.KEY_KNN_N_NEIGHBORS: 10,
	P.KEY_PRE_NET_MODULES: ['models.gdes.model_6l.Net'],
	P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/base/config_gdes/iter' + P.STR_TOKEN + '/models/model0.pt'],
	P.KEY_PRE_NET_OUTPUTS: ['bn5'],
}

btmupexp_fc_on_hebb_layer = {
    P.KEY_EXPERIMENT: 'neurolab.experiment.btmupexp.BtmUpExperiment',
    P.KEY_SUBCONFIG_LIST: ['configs.base.config_hebb', 'configs.base.fc_on_hebb_layer'],
    'exp1::' + P.KEY_PRE_NET_MDL_PATHS: ['exp0/iter' + P.STR_TOKEN + '/models/model0.pt'],
    P.KEY_HPMANAGER: 'neurolab.hpsearch.DiscAltMinHPManager',
    P.KEY_HPSEARCH_PARAMS: {'exp0+exp1::' + P.KEY_LEARNING_RATE: [1e-4, 1e-3], 'exp0::' + P.KEY_L2_PENALTY: [5e-2, 5e-3, 5e-4], 'exp1::' + P.KEY_L2_PENALTY: [5e-2, 5e-3, 5e-4]},
}

config_vae = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.AEVisionExperiment',
	P.KEY_NET_MODULES: 'models.gdes.vae_6l.Net',
	P.KEY_NET_OUTPUTS: 'vae_output',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20, #40,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
	P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.ELBOMetricManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.ELBOMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
    P.KEY_LR_DECAY: 0.5, #0.1,
    P.KEY_MILESTONES: range(10, 20), #[20, 30],
    P.KEY_MOMENTUM: 0.9,
	P.KEY_ELBO_BETA: .5,
}

config_stackvae = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'models.gdes.stackvae_6l.Net',
	P.KEY_NET_OUTPUTS: 'fc6',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20, #40,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
	P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
    P.KEY_LR_DECAY: 0.5, #0.1,
    P.KEY_MILESTONES: range(10, 20), #[20, 30],
    P.KEY_MOMENTUM: 0.9,
	P.KEY_ELBO_BETA: .5,
}

fc_on_stackvae_layer = {
	P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
	P.KEY_NET_MODULES: 'models.gdes.fc.Net',
	P.KEY_NET_OUTPUTS: 'fc',
	P.KEY_DATA_MANAGER: 'neurolab.data.CIFAR10DataManager',
	P.KEY_AUGMENT_MANAGER: None, #'neurolab.data.LightCustomAugmentManager',
	P.KEY_AUGM_STAT_PASSES: 2,
	P.KEY_AUGM_BEFORE_STATS: True,
	P.KEY_WHITEN: None,
	P.KEY_TOT_TRN_SAMPLES: 40000,
	P.KEY_BATCHSIZE: 64,
	P.KEY_INPUT_SHAPE: (3, 32, 32),
	P.KEY_NUM_EPOCHS: 20, #40,
	P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
	P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
	P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
	P.KEY_CRIT_METRIC_MANAGER: 'neurolab.optimization.metric.AccMetricManager',
    P.KEY_LEARNING_RATE: 1e-3,
    P.KEY_LR_DECAY: 0.5, #0.1,
    P.KEY_MILESTONES: range(10, 20), #[20, 30],
    P.KEY_MOMENTUM: 0.9,
    P.KEY_L2_PENALTY: 5e-4,
	P.KEY_DROPOUT_P: 0.5,
	P.KEY_PRE_NET_MODULES: ['models.gdes.stackvae_6l.Net'],
	P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/base/config_stackvae/iter' + P.STR_TOKEN + '/models/model0.pt'],
	P.KEY_PRE_NET_OUTPUTS: ['bn5'],
	P.KEY_ELBO_BETA: .5,
}

