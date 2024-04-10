package catboost

import (
	"encoding/json"
	"fmt"
)

type MetaInfo interface {
	get(cStrings string) error
}

type ClassParams struct {
	ClassesCount   int    `json:"classes_count"`
	ClassNames     []int  `json:"class_names"`
	ClassToLabel   []int  `json:"class_to_label"`
	ClassLabelType string `json:"class_label_type"`
}

func (m *ClassParams) get(cStrings string) error {
	err := json.Unmarshal([]byte(cStrings), &m)
	if err != nil {
		fmt.Println(err)
		return err
	}
	return nil
}

type OutputOptions struct {
	Name                              string   `json:"name"`
	Verbose                           int      `json:"verbose"`
	TestErrorLog                      string   `json:"test_error_log"`
	JsonLog                           string   `json:"json_log"`
	ResultModelFile                   string   `json:"result_model_file"`
	RocFile                           string   `json:"roc_file"`
	EvalFileName                      string   `json:"eval_file_name"`
	UseBestModel                      bool     `json:"use_best_model"`
	AllowWritingFiles                 bool     `json:"allow_writing_files"`
	PredictionType                    []string `json:"prediction_type"`
	FstrInternalFile                  string   `json:"fstr_internal_file"`
	OutputColumns                     []string `json:"output_columns"`
	SnapshotInterval                  int      `json:"snapshot_interval"`
	TimeLeftLog                       string   `json:"time_left_log"`
	FstrType                          string   `json:"fstr_type"`
	ProfileLog                        string   `json:"profile_log"`
	TrainDir                          string   `json:"train_dir"`
	LearnErrorLog                     string   `json:"learn_error_log"`
	TrainingOptionsFile               string   `json:"training_options_file"`
	SnapshotFile                      string   `json:"snapshot_file"`
	SaveSnapshot                      bool     `json:"save_snapshot"`
	ModelFormat                       []string `json:"model_format"`
	FinalFeatureCalcerComputationMode string   `json:"final_feature_calcer_computation_mode"`
	MetricPeriod                      int      `json:"metric_period"`
	OutputBorders                     string   `json:"output_borders"`
	FinalCtrComputationMode           string   `json:"final_ctr_computation_mode"`
	BestModelMinTrees                 int      `json:"best_model_min_trees"`
	FstrRegularFile                   string   `json:"fstr_regular_file"`
}

func (o *OutputOptions) get(cStrings string) error {
	err := json.Unmarshal([]byte(cStrings), &o)
	if err != nil {
		fmt.Println(err)
		return err
	}
	return nil
}

type Params struct {
	DetailedProfile bool `json:"detailed_profile"`
	BoostingOptions struct {
		ModelShrinkMode      string `json:"model_shrink_mode"`
		ApproxOnFullHistory  bool   `json:"approx_on_full_history"`
		FoldLenMultiplier    int    `json:"fold_len_multiplier"`
		FoldPermutationBlock int    `json:"fold_permutation_block"`
		PosteriorSampling    bool   `json:"posterior_sampling"`
		BoostingType         string `json:"boosting_type"`
		Iterations           int    `json:"iterations"`
		ModelShrinkRate      int    `json:"model_shrink_rate"`
		BoostFromAverage     bool   `json:"boost_from_average"`
		OdConfig             struct {
			WaitIterations int    `json:"wait_iterations"`
			Type           string `json:"type"`
			StopPvalue     int    `json:"stop_pvalue"`
		} `json:"od_config"`
		PermutationCount int     `json:"permutation_count"`
		LearningRate     float64 `json:"learning_rate"`
	} `json:"boosting_options"`
	PoolMetainfoOptions struct {
		Tags struct {
		} `json:"tags"`
	} `json:"pool_metainfo_options"`
	Metadata struct {
	} `json:"metadata"`
	Metrics struct {
		EvalMetric struct {
			Type   string `json:"type"`
			Params struct {
			} `json:"params"`
		} `json:"eval_metric"`
		ObjectiveMetric struct {
			Type   string `json:"type"`
			Params struct {
			} `json:"params"`
		} `json:"objective_metric"`
		CustomMetrics []interface{} `json:"custom_metrics"`
	} `json:"metrics"`
	CatFeatureParams struct {
		StoreAllSimpleCtr bool    `json:"store_all_simple_ctr"`
		CtrLeafCountLimit float64 `json:"ctr_leaf_count_limit"`
		SimpleCtrs        []struct {
			CtrBinarization struct {
				BorderCount int    `json:"border_count"`
				BorderType  string `json:"border_type"`
			} `json:"ctr_binarization"`
			TargetBinarization struct {
				BorderCount int    `json:"border_count"`
				BorderType  string `json:"border_type"`
			} `json:"target_binarization,omitempty"`
			CtrType         string      `json:"ctr_type"`
			Priors          [][]float64 `json:"priors"`
			PriorEstimation string      `json:"prior_estimation"`
		} `json:"simple_ctrs"`
		CounterCalcMethod  string `json:"counter_calc_method"`
		OneHotMaxSize      int    `json:"one_hot_max_size"`
		MaxCtrComplexity   int    `json:"max_ctr_complexity"`
		TargetBinarization struct {
			BorderCount int    `json:"border_count"`
			BorderType  string `json:"border_type"`
		} `json:"target_binarization"`
		CombinationsCtrs []struct {
			CtrBinarization struct {
				BorderCount int    `json:"border_count"`
				BorderType  string `json:"border_type"`
			} `json:"ctr_binarization"`
			TargetBinarization struct {
				BorderCount int    `json:"border_count"`
				BorderType  string `json:"border_type"`
			} `json:"target_binarization,omitempty"`
			CtrType         string      `json:"ctr_type"`
			Priors          [][]float64 `json:"priors"`
			PriorEstimation string      `json:"prior_estimation"`
		} `json:"combinations_ctrs"`
		PerFeatureCtrs struct {
		} `json:"per_feature_ctrs"`
	} `json:"cat_feature_params"`
	LoggingLevel       string `json:"logging_level"`
	TreeLearnerOptions struct {
		SamplingFrequency   string  `json:"sampling_frequency"`
		ModelSizeReg        float64 `json:"model_size_reg"`
		BayesianMatrixReg   float64 `json:"bayesian_matrix_reg"`
		ScoreFunction       string  `json:"score_function"`
		MonotoneConstraints struct {
		} `json:"monotone_constraints"`
		LeafEstimationMethod     string `json:"leaf_estimation_method"`
		DevScoreCalcObjBlockSize int    `json:"dev_score_calc_obj_block_size"`
		GrowPolicy               string `json:"grow_policy"`
		MinDataInLeaf            int    `json:"min_data_in_leaf"`
		RandomStrength           int    `json:"random_strength"`
		DevEfbMaxBuckets         int    `json:"dev_efb_max_buckets"`
		L2LeafReg                int    `json:"l2_leaf_reg"`
		Bootstrap                struct {
			BaggingTemperature int    `json:"bagging_temperature"`
			Type               string `json:"type"`
		} `json:"bootstrap"`
		Depth                      int    `json:"depth"`
		MaxLeaves                  int    `json:"max_leaves"`
		LeafEstimationBacktracking string `json:"leaf_estimation_backtracking"`
		Rsm                        int    `json:"rsm"`
		DevLeafwiseApproxes        bool   `json:"dev_leafwise_approxes"`
		LeafEstimationIterations   int    `json:"leaf_estimation_iterations"`
		Penalties                  struct {
			FirstFeatureUsePenalties struct {
			} `json:"first_feature_use_penalties"`
			PerObjectFeaturePenalties struct {
			} `json:"per_object_feature_penalties"`
			FeatureWeights struct {
			} `json:"feature_weights"`
			PenaltiesCoefficient int `json:"penalties_coefficient"`
		} `json:"penalties"`
		SparseFeaturesConflictFraction int `json:"sparse_features_conflict_fraction"`
	} `json:"tree_learner_options"`
	LossFunction struct {
		Type   string `json:"type"`
		Params struct {
		} `json:"params"`
	} `json:"loss_function"`
	DataProcessingOptions struct {
		IgnoredFeatures           []interface{} `json:"ignored_features"`
		FloatFeaturesBinarization struct {
			BorderCount                     int    `json:"border_count"`
			DevMaxSubsetSizeForBuildBorders int    `json:"dev_max_subset_size_for_build_borders"`
			NanMode                         string `json:"nan_mode"`
			BorderType                      string `json:"border_type"`
		} `json:"float_features_binarization"`
		HasTime                          bool    `json:"has_time"`
		DevSparseArrayIndexing           string  `json:"dev_sparse_array_indexing"`
		AllowConstLabel                  bool    `json:"allow_const_label"`
		DevDefaultValueFractionForSparse float64 `json:"dev_default_value_fraction_for_sparse"`
		ClassNames                       []int   `json:"class_names"`
		EmbeddingProcessingOptions       struct {
			EmbeddingProcessing struct {
				Default []string `json:"default"`
			} `json:"embedding_processing"`
		} `json:"embedding_processing_options"`
		DevGroupFeatures            bool        `json:"dev_group_features"`
		EvalFraction                int         `json:"eval_fraction"`
		ClassesCount                int         `json:"classes_count"`
		DevLeafwiseScoring          bool        `json:"dev_leafwise_scoring"`
		AutoClassWeights            string      `json:"auto_class_weights"`
		TargetBorder                interface{} `json:"target_border"`
		ForceUnitAutoPairWeights    bool        `json:"force_unit_auto_pair_weights"`
		PerFloatFeatureQuantization struct {
		} `json:"per_float_feature_quantization"`
		TextProcessingOptions struct {
			Dictionaries []struct {
				StartTokenId             string `json:"start_token_id"`
				OccurrenceLowerBound     string `json:"occurrence_lower_bound"`
				SkipStep                 string `json:"skip_step"`
				EndOfWordTokenPolicy     string `json:"end_of_word_token_policy"`
				TokenLevelType           string `json:"token_level_type"`
				EndOfSentenceTokenPolicy string `json:"end_of_sentence_token_policy"`
				GramOrder                string `json:"gram_order"`
				MaxDictionarySize        string `json:"max_dictionary_size"`
				DictionaryId             string `json:"dictionary_id"`
			} `json:"dictionaries"`
			FeatureProcessing struct {
				Default []struct {
					DictionariesNames []string `json:"dictionaries_names"`
					FeatureCalcers    []string `json:"feature_calcers"`
					TokenizersNames   []string `json:"tokenizers_names"`
				} `json:"default"`
			} `json:"feature_processing"`
			Tokenizers []struct {
				NumberToken         string        `json:"number_token"`
				SkipEmpty           string        `json:"skip_empty"`
				NumberProcessPolicy string        `json:"number_process_policy"`
				TokenizerId         string        `json:"tokenizer_id"`
				TokenTypes          []string      `json:"token_types"`
				Delimiter           string        `json:"delimiter"`
				Languages           []interface{} `json:"languages"`
				Lemmatizing         string        `json:"lemmatizing"`
				SplitBySet          string        `json:"split_by_set"`
				Lowercasing         string        `json:"lowercasing"`
				SubtokensPolicy     string        `json:"subtokens_policy"`
				SeparatorType       string        `json:"separator_type"`
			} `json:"tokenizers"`
		} `json:"text_processing_options"`
		ClassWeights []interface{} `json:"class_weights"`
	} `json:"data_processing_options"`
	TaskType   string `json:"task_type"`
	FlatParams struct {
		EvalMetric   string  `json:"eval_metric"`
		Depth        int     `json:"depth"`
		RandomSeed   int     `json:"random_seed"`
		LossFunction string  `json:"loss_function"`
		LearningRate float64 `json:"learning_rate"`
		Iterations   int     `json:"iterations"`
		Verbose      int     `json:"verbose"`
	} `json:"flat_params"`
	SystemOptions struct {
		ThreadCount   int    `json:"thread_count"`
		FileWithHosts string `json:"file_with_hosts"`
		NodeType      string `json:"node_type"`
		UsedRamLimit  string `json:"used_ram_limit"`
		NodePort      int    `json:"node_port"`
	} `json:"system_options"`
	RandomSeed int `json:"random_seed"`
}

func (p *Params) get(cStrings string) error {
	err := json.Unmarshal([]byte(cStrings), &p)
	if err != nil {
		fmt.Println(err)
		return err
	}
	return nil
}

func Get(cStrings string, meta MetaInfo) error {
	err := meta.get(cStrings)
	if err != nil {
		return err
	}
	return nil
}
