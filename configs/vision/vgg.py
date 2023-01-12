from neurolab import params as P
import params as PP
from .meta import *


config_base_hebb_vgg = {}
gdes_fc_on_hebb_vgg_ft = {}
gdes_fc2_on_hebb_vgg_ft = {}
prec_on_hebb_vgg_ft = {}
smpleff_gdes_fc_on_hebb_vgg_ft = {}
smpleff_gdes_fc2_on_hebb_vgg_ft = {}
smpleff_prec_on_hebb_vgg_ft = {}

for ds in datasets:
	for da in da_strategies:
		for lrn_rule in lrn_rules:
			config_base_hebb_vgg[lrn_rule + '_' + ds + da_names[da]] = {
				P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
				P.KEY_NET_MODULES: 'models.hebb.vgg.Net',
				P.KEY_NET_OUTPUTS: 'clf',
				P.KEY_DATA_MANAGER: data_managers[ds],
				P.KEY_AUGMENT_MANAGER: da_managers[da],
				P.KEY_AUGM_BEFORE_STATS: True,
				P.KEY_AUGM_STAT_PASSES: da_mult[da],
				P.KEY_WHITEN: None if lrn_rule_keys[lrn_rule] != 'hwta' else 2,
				P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
				P.KEY_BATCHSIZE: 32,
				P.KEY_INPUT_SHAPE: (3, 224, 224),
				P.KEY_NUM_EPOCHS: 20,
				P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
				P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
				P.KEY_TOPKACC_K: [1, 5],
			    P.KEY_LEARNING_RATE: hebb_lrn_rates[lrn_rule_keys[lrn_rule]][ds],
				P.KEY_LOCAL_LRN_RULE: lrn_rule_keys[lrn_rule],
				PP.KEY_COMPETITIVE_ACT: lrn_rule_competitive_act[lrn_rule],
				PP.KEY_COMPETITIVE_K: lrn_rule_k[lrn_rule],
				P.KEY_DEEP_TEACHER_SIGNAL: lrn_rule_dts[lrn_rule],
			}
		
			gdes_fc_on_hebb_vgg_ft[lrn_rule + '_' + ds + da_names[da]] = {
				P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
				P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc.Net'],
				P.KEY_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/config_base_hebb_vgg[' + lrn_rule + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt'],
				P.KEY_NET_OUTPUTS: ['conv_output', 'fc'],
				P.KEY_DATA_MANAGER: data_managers[ds],
				P.KEY_AUGMENT_MANAGER: da_managers[da],
				P.KEY_AUGM_BEFORE_STATS: True,
				P.KEY_AUGM_STAT_PASSES: da_mult[da],
				P.KEY_WHITEN: None if lrn_rule_keys[lrn_rule] != 'hwta' else 2,
				P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
				P.KEY_BATCHSIZE: 32,
				P.KEY_INPUT_SHAPE: (3, 224, 224),
				P.KEY_NUM_EPOCHS: da_mult[da] * 20,
				P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
				P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
				P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
				P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
				P.KEY_TOPKACC_K: [1, 5],
			    P.KEY_LEARNING_RATE: 1e-3,
				P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
			    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
	            P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
			    P.KEY_MOMENTUM: 0.9,
			    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
				P.KEY_DROPOUT_P: 0.5,
				P.KEY_LOCAL_LRN_RULE: lrn_rule_keys[lrn_rule],
				PP.KEY_COMPETITIVE_ACT: lrn_rule_competitive_act[lrn_rule],
				PP.KEY_COMPETITIVE_K: lrn_rule_k[lrn_rule],
				P.KEY_DEEP_TEACHER_SIGNAL: lrn_rule_dts[lrn_rule],
			}
			
			gdes_fc2_on_hebb_vgg_ft[lrn_rule + '_' + ds + da_names[da]] = {
				P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
				P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
				P.KEY_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/config_base_hebb_vgg[' + lrn_rule + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt'],
				P.KEY_NET_OUTPUTS: ['conv_output', 'fc2'],
				P.KEY_DATA_MANAGER: data_managers[ds],
				P.KEY_AUGMENT_MANAGER: da_managers[da],
				P.KEY_AUGM_BEFORE_STATS: True,
				P.KEY_AUGM_STAT_PASSES: da_mult[da],
				P.KEY_WHITEN: None if lrn_rule_keys[lrn_rule] != 'hwta' else 2,
				P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
				P.KEY_BATCHSIZE: 32,
				P.KEY_INPUT_SHAPE: (3, 224, 224),
				P.KEY_NUM_EPOCHS: da_mult[da] * 20,
				P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
				P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
				P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
				P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
				P.KEY_TOPKACC_K: [1, 5],
			    P.KEY_LEARNING_RATE: 1e-3,
				P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
			    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
	            P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
			    P.KEY_MOMENTUM: 0.9,
			    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
				P.KEY_DROPOUT_P: 0.5,
				P.KEY_LOCAL_LRN_RULE: lrn_rule_keys[lrn_rule],
				PP.KEY_COMPETITIVE_ACT: lrn_rule_competitive_act[lrn_rule],
				PP.KEY_COMPETITIVE_K: lrn_rule_k[lrn_rule],
				P.KEY_DEEP_TEACHER_SIGNAL: lrn_rule_dts[lrn_rule],
			}
			
			prec_on_hebb_vgg_ft[lrn_rule + '_' + ds + da_names[da]] = {
				P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
				P.KEY_NET_MODULES: 'neurolab.model.skclassif.Retriever',
				P.KEY_NET_OUTPUTS: 'clf',
				P.KEY_DATA_MANAGER: data_managers[ds],
				P.KEY_AUGMENT_MANAGER: None,
				P.KEY_AUGM_BEFORE_STATS: True,
				P.KEY_AUGM_STAT_PASSES: da_mult[da],
				P.KEY_WHITEN: None if lrn_rule_keys[lrn_rule] != 'hwta' else 2,
				P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
				P.KEY_NUM_TRN_SAMPLES: retr_num_samples[ds],
				P.KEY_BATCHSIZE: 32,
				P.KEY_INPUT_SHAPE: (3, 224, 224),
				P.KEY_NUM_EPOCHS: 1,
				P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.PrecMetricManager', 'neurolab.optimization.metric.MAPMetricManager'] * len(retr_k[ds]),
				P.KEY_SKCLF_NUM_SAMPLES: retr_num_samples[ds],
				P.KEY_NYSTROEM_N_COMPONENTS: retr_num_nyst[ds],
				P.KEY_KNN_N_NEIGHBORS: retr_num_rel[ds],
				P.KEY_RETR_NUM_REL: retr_num_rel[ds],
				P.KEY_RETR_K: retr_k[ds],
				P.KEY_LOCAL_LRN_RULE: lrn_rule_keys[lrn_rule],
				PP.KEY_COMPETITIVE_ACT: lrn_rule_competitive_act[lrn_rule],
				PP.KEY_COMPETITIVE_K: lrn_rule_k[lrn_rule],
				P.KEY_PRE_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
				P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/gdes_fc2_on_hebb_vgg_ft[' + lrn_rule + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt',
				                          P.PROJECT_ROOT + '/results/configs/vision/vgg/gdes_fc2_on_hebb_vgg_ft[' + lrn_rule + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model1.pt'],
				P.KEY_PRE_NET_OUTPUTS: ['conv_output', 'bn1'],
			}
			
			for n in smpleff_regimes[ds]:
				for lrn_rule in lrn_rules:
					
					smpleff_gdes_fc_on_hebb_vgg_ft[lrn_rule + '_' + ds + '_' + str(n) + da_names[da]] = {
						P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
						P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc.Net'],
						P.KEY_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/config_base_hebb_vgg[' + lrn_rule + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt'],
						P.KEY_NET_OUTPUTS: ['conv_output', 'fc'],
						P.KEY_DATA_MANAGER: data_managers[ds],
						P.KEY_AUGMENT_MANAGER: da_managers[da],
						P.KEY_AUGM_BEFORE_STATS: True,
						P.KEY_AUGM_STAT_PASSES: da_mult[da],
						P.KEY_WHITEN: None if lrn_rule_keys[lrn_rule] != 'hwta' else 2,
						P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds], P.KEY_NUM_TRN_SAMPLES: n,
						P.KEY_BATCHSIZE: 32,
						P.KEY_INPUT_SHAPE: (3, 224, 224),
						P.KEY_NUM_EPOCHS: da_mult[da] * 20,
						P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
						P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
						P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
						P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
						P.KEY_TOPKACC_K: [1, 5],
					    P.KEY_LEARNING_RATE: 1e-3,
						P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
					    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
		                P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
					    P.KEY_MOMENTUM: 0.9,
					    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
						P.KEY_DROPOUT_P: 0.5,
						P.KEY_LOCAL_LRN_RULE: lrn_rule_keys[lrn_rule],
						PP.KEY_COMPETITIVE_ACT: lrn_rule_competitive_act[lrn_rule],
						PP.KEY_COMPETITIVE_K: lrn_rule_k[lrn_rule],
					}
					
					smpleff_gdes_fc2_on_hebb_vgg_ft[lrn_rule + '_' + ds + '_' + str(n) + da_names[da]] = {
						P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
						P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
						P.KEY_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/config_base_hebb_vgg[' + lrn_rule + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt'],
						P.KEY_NET_OUTPUTS: ['conv_output', 'fc2'],
						P.KEY_DATA_MANAGER: data_managers[ds],
						P.KEY_AUGMENT_MANAGER: da_managers[da],
						P.KEY_AUGM_BEFORE_STATS: True,
						P.KEY_AUGM_STAT_PASSES: da_mult[da],
						P.KEY_WHITEN: None if lrn_rule_keys[lrn_rule] != 'hwta' else 2,
						P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds], P.KEY_NUM_TRN_SAMPLES: n,
						P.KEY_BATCHSIZE: 32,
						P.KEY_INPUT_SHAPE: (3, 224, 224),
						P.KEY_NUM_EPOCHS: da_mult[da] * 20,
						P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
						P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
						P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
						P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
						P.KEY_TOPKACC_K: [1, 5],
					    P.KEY_LEARNING_RATE: 1e-3,
						P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
					    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
		                P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
					    P.KEY_MOMENTUM: 0.9,
					    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
						P.KEY_DROPOUT_P: 0.5,
						P.KEY_LOCAL_LRN_RULE: lrn_rule_keys[lrn_rule],
						PP.KEY_COMPETITIVE_ACT: lrn_rule_competitive_act[lrn_rule],
						PP.KEY_COMPETITIVE_K: lrn_rule_k[lrn_rule],
					}
					
					smpleff_prec_on_hebb_vgg_ft[lrn_rule + '_' + ds + '_' + str(n) + da_names[da]] = {
						P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
						P.KEY_NET_MODULES: 'neurolab.model.skclassif.Retriever',
						P.KEY_NET_OUTPUTS: 'clf',
						P.KEY_DATA_MANAGER: data_managers[ds],
						P.KEY_AUGMENT_MANAGER: None,
						P.KEY_AUGM_STAT_PASSES: da_mult[da],
						P.KEY_AUGM_BEFORE_STATS: True,
						P.KEY_WHITEN: None if lrn_rule_keys[lrn_rule] != 'hwta' else 2,
						P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
						P.KEY_NUM_TRN_SAMPLES: retr_num_samples[ds],
						P.KEY_BATCHSIZE: 32,
						P.KEY_INPUT_SHAPE: (3, 224, 224),
						P.KEY_NUM_EPOCHS: 1,
						P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.PrecMetricManager', 'neurolab.optimization.metric.MAPMetricManager'] * len(retr_k[ds]),
						P.KEY_SKCLF_NUM_SAMPLES: retr_num_samples[ds],
						P.KEY_NYSTROEM_N_COMPONENTS: retr_num_nyst[ds],
						P.KEY_KNN_N_NEIGHBORS: retr_num_rel[ds],
						P.KEY_RETR_NUM_REL: retr_num_rel[ds],
						P.KEY_RETR_K: retr_k[ds],
						P.KEY_LOCAL_LRN_RULE: lrn_rule_keys[lrn_rule],
						PP.KEY_COMPETITIVE_ACT: lrn_rule_competitive_act[lrn_rule],
						PP.KEY_COMPETITIVE_K: lrn_rule_k[lrn_rule],
						P.KEY_PRE_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
						P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/smpleff_gdes_fc2_on_hebb_vgg_ft[' + lrn_rule + '_' + ds + '_' + str(n) + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt',
						                          P.PROJECT_ROOT + '/results/configs/vision/vgg/smpleff_gdes_fc2_on_hebb_vgg_ft[' + lrn_rule + '_' + ds + '_' + str(n) + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model1.pt'],
						P.KEY_PRE_NET_OUTPUTS: ['conv_output', 'bn1'],
					}
			
		gdes_fc_on_hebb_vgg_ft['none' + '_' + ds + da_names[da]] = {
			P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
			P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc.Net'],
			P.KEY_NET_MDL_PATHS: None,
			P.KEY_NET_OUTPUTS: ['conv_output', 'fc'],
			P.KEY_DATA_MANAGER: data_managers[ds],
			P.KEY_AUGMENT_MANAGER: da_managers[da],
			P.KEY_AUGM_BEFORE_STATS: True,
			P.KEY_AUGM_STAT_PASSES: da_mult[da],
			P.KEY_WHITEN: None,
			P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
			P.KEY_BATCHSIZE: 32,
			P.KEY_INPUT_SHAPE: (3, 224, 224),
			P.KEY_NUM_EPOCHS: da_mult[da] * 20,
			P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
			P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
			P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
			P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
			P.KEY_TOPKACC_K: [1, 5],
		    P.KEY_LEARNING_RATE: 1e-3,
			P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
		    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
            P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
		    P.KEY_MOMENTUM: 0.9,
		    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
			P.KEY_DROPOUT_P: 0.5,
			P.KEY_LOCAL_LRN_RULE: 'none',
			PP.KEY_COMPETITIVE_ACT: None,
			PP.KEY_COMPETITIVE_K: 0,
			P.KEY_DEEP_TEACHER_SIGNAL: False,
		}
		
		gdes_fc2_on_hebb_vgg_ft['none' + '_' + ds + da_names[da]] = {
			P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
			P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
			P.KEY_NET_MDL_PATHS: None,
			P.KEY_NET_OUTPUTS: ['conv_output', 'fc2'],
			P.KEY_DATA_MANAGER: data_managers[ds],
			P.KEY_AUGMENT_MANAGER: da_managers[da],
			P.KEY_AUGM_BEFORE_STATS: True,
			P.KEY_AUGM_STAT_PASSES: da_mult[da],
			P.KEY_WHITEN: None,
			P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
			P.KEY_BATCHSIZE: 32,
			P.KEY_INPUT_SHAPE: (3, 224, 224),
			P.KEY_NUM_EPOCHS: da_mult[da] * 20,
			P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
			P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
			P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
			P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
			P.KEY_TOPKACC_K: [1, 5],
		    P.KEY_LEARNING_RATE: 1e-3,
			P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
		    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
            P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
		    P.KEY_MOMENTUM: 0.9,
		    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
			P.KEY_DROPOUT_P: 0.5,
			P.KEY_LOCAL_LRN_RULE: 'none',
			PP.KEY_COMPETITIVE_ACT: None,
			PP.KEY_COMPETITIVE_K: 0,
			P.KEY_DEEP_TEACHER_SIGNAL: False,
		}
		
		prec_on_hebb_vgg_ft['none' + '_' + ds + da_names[da]] = {
			P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
			P.KEY_NET_MODULES: 'neurolab.model.skclassif.Retriever',
			P.KEY_NET_OUTPUTS: 'clf',
			P.KEY_DATA_MANAGER: data_managers[ds],
			P.KEY_AUGMENT_MANAGER: None,
			P.KEY_AUGM_BEFORE_STATS: True,
			P.KEY_AUGM_STAT_PASSES: da_mult[da],
			P.KEY_WHITEN: None,
			P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
			P.KEY_NUM_TRN_SAMPLES: retr_num_samples[ds],
			P.KEY_BATCHSIZE: 32,
			P.KEY_INPUT_SHAPE: (3, 224, 224),
			P.KEY_NUM_EPOCHS: 1,
			P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.PrecMetricManager', 'neurolab.optimization.metric.MAPMetricManager'] * len(retr_k[ds]),
			P.KEY_SKCLF_NUM_SAMPLES: retr_num_samples[ds],
			P.KEY_NYSTROEM_N_COMPONENTS: retr_num_nyst[ds],
			P.KEY_KNN_N_NEIGHBORS: retr_num_rel[ds],
			P.KEY_RETR_NUM_REL: retr_num_rel[ds],
			P.KEY_RETR_K: retr_k[ds],
			P.KEY_LOCAL_LRN_RULE: 'none',
			PP.KEY_COMPETITIVE_ACT: None,
			PP.KEY_COMPETITIVE_K: 0,
			P.KEY_PRE_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
			P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/gdes_fc2_on_hebb_vgg_ft[' + 'none' + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt',
			                          P.PROJECT_ROOT + '/results/configs/vision/vgg/gdes_fc2_on_hebb_vgg_ft[' + 'none' + '_' + ds + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model1.pt'],
			P.KEY_PRE_NET_OUTPUTS: ['conv_output', 'bn1'],
		}
		
		for n in smpleff_regimes[ds]:
			for lrn_rule in lrn_rules:
				
				smpleff_gdes_fc_on_hebb_vgg_ft['none' + '_' + ds + '_' + str(n) + da_names[da]] = {
					P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
					P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc.Net'],
					P.KEY_NET_MDL_PATHS: None,
					P.KEY_NET_OUTPUTS: ['conv_output', 'fc'],
					P.KEY_DATA_MANAGER: data_managers[ds],
					P.KEY_AUGMENT_MANAGER: da_managers[da],
					P.KEY_AUGM_BEFORE_STATS: True,
					P.KEY_AUGM_STAT_PASSES: da_mult[da],
					P.KEY_WHITEN: None,
					P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds], P.KEY_NUM_TRN_SAMPLES: n,
					P.KEY_BATCHSIZE: 32,
					P.KEY_INPUT_SHAPE: (3, 224, 224),
					P.KEY_NUM_EPOCHS: da_mult[da] * 20,
					P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
					P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
					P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
					P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
					P.KEY_TOPKACC_K: [1, 5],
				    P.KEY_LEARNING_RATE: 1e-3,
					P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
				    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
	                P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
				    P.KEY_MOMENTUM: 0.9,
				    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
					P.KEY_DROPOUT_P: 0.5,
					P.KEY_LOCAL_LRN_RULE: 'none',
					PP.KEY_COMPETITIVE_ACT: None,
					PP.KEY_COMPETITIVE_K: 0,
				}
				
				smpleff_gdes_fc2_on_hebb_vgg_ft['none' + '_' + ds + '_' + str(n) + da_names[da]] = {
					P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
					P.KEY_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
					P.KEY_NET_MDL_PATHS: None,
					P.KEY_NET_OUTPUTS: ['conv_output', 'fc2'],
					P.KEY_DATA_MANAGER: data_managers[ds],
					P.KEY_AUGMENT_MANAGER: da_managers[da],
					P.KEY_AUGM_BEFORE_STATS: True,
					P.KEY_AUGM_STAT_PASSES: da_mult[da],
					P.KEY_WHITEN: None,
					P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds], P.KEY_NUM_TRN_SAMPLES: n,
					P.KEY_BATCHSIZE: 32,
					P.KEY_INPUT_SHAPE: (3, 224, 224),
					P.KEY_NUM_EPOCHS: da_mult[da] * 20,
					P.KEY_OPTIM_MANAGER: 'neurolab.optimization.optim.SGDOptimManager',
					P.KEY_SCHED_MANAGER: 'neurolab.optimization.sched.MultiStepSchedManager',
					P.KEY_LOSS_METRIC_MANAGER: 'neurolab.optimization.metric.CrossEntMetricManager',
					P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.TopKAccMetricManager', 'neurolab.optimization.metric.TopKAccMetricManager'],
					P.KEY_TOPKACC_K: [1, 5],
				    P.KEY_LEARNING_RATE: 1e-3,
					P.KEY_ALPHA_L: 0, P.KEY_ALPHA_G: 1,
				    P.KEY_LR_DECAY: 0.5 if da == 'no_da' else 0.1,
	                P.KEY_MILESTONES: range(10, 20) if da == 'no_da' else [20, 30] if da == 'light_da' else [40, 70, 90],
				    P.KEY_MOMENTUM: 0.9,
				    P.KEY_L2_PENALTY: l2_penalties[ds + da_names[da]],
					P.KEY_DROPOUT_P: 0.5,
					P.KEY_LOCAL_LRN_RULE: 'none',
					PP.KEY_COMPETITIVE_ACT: None,
					PP.KEY_COMPETITIVE_K: 0,
				}
				
				smpleff_prec_on_hebb_vgg_ft['none' + '_' + ds + '_' + str(n) + da_names[da]] = {
					P.KEY_EXPERIMENT: 'neurolab.experiment.VisionExperiment',
					P.KEY_NET_MODULES: 'neurolab.model.skclassif.Retriever',
					P.KEY_NET_OUTPUTS: 'clf',
					P.KEY_DATA_MANAGER: data_managers[ds],
					P.KEY_AUGMENT_MANAGER: None,
					P.KEY_AUGM_STAT_PASSES: da_mult[da],
					P.KEY_AUGM_BEFORE_STATS: True,
					P.KEY_WHITEN: None,
					P.KEY_TOT_TRN_SAMPLES: tot_trn_samples[ds],
					P.KEY_NUM_TRN_SAMPLES: retr_num_samples[ds],
					P.KEY_BATCHSIZE: 32,
					P.KEY_INPUT_SHAPE: (3, 224, 224),
					P.KEY_NUM_EPOCHS: 1,
					P.KEY_CRIT_METRIC_MANAGER: ['neurolab.optimization.metric.PrecMetricManager', 'neurolab.optimization.metric.MAPMetricManager'] * len(retr_k[ds]),
					P.KEY_SKCLF_NUM_SAMPLES: retr_num_samples[ds],
					P.KEY_NYSTROEM_N_COMPONENTS: retr_num_nyst[ds],
					P.KEY_KNN_N_NEIGHBORS: retr_num_rel[ds],
					P.KEY_RETR_NUM_REL: retr_num_rel[ds],
					P.KEY_RETR_K: retr_k[ds],
					P.KEY_LOCAL_LRN_RULE: 'none',
					PP.KEY_COMPETITIVE_ACT: None,
					PP.KEY_COMPETITIVE_K: 0,
					P.KEY_PRE_NET_MODULES: ['models.hebb.vgg.Net', 'models.gdes.fc2.Net'], 'mdl1:' + PP.KEY_NUM_HIDDEN: 256,
					P.KEY_PRE_NET_MDL_PATHS: [P.PROJECT_ROOT + '/results/configs/vision/vgg/smpleff_gdes_fc2_on_hebb_vgg_ft[' + 'none' + '_' + ds + '_' + str(n) + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model0.pt',
					                          P.PROJECT_ROOT + '/results/configs/vision/vgg/smpleff_gdes_fc2_on_hebb_vgg_ft[' + 'none' + '_' + ds + '_' + str(n) + da_names[da] + ']/iter' + P.STR_TOKEN + '/models/model1.pt'],
					P.KEY_PRE_NET_OUTPUTS: ['conv_output', 'bn1'],
				}
		
		