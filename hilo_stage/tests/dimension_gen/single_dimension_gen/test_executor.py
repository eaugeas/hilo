import unittest

from tensorflow_metadata.proto.v0.statistics_pb2 import (
    CommonStatistics, DatasetFeatureStatisticsList,
    DatasetFeatureStatistics, FeatureNameStatistics,
    NumericStatistics)

from hilo_stage.dimension_gen.single_dimension_gen.executor import (
    infer_dimensions)


class InferDimensionsTest(unittest.TestCase):
    def test_infer_dimensions_ok_one_feature(self):
        datasets = infer_dimensions(DatasetFeatureStatisticsList(datasets=[
            DatasetFeatureStatistics(
                num_examples=10,
                features=[FeatureNameStatistics(
                    name='feature_name',
                    num_stats=NumericStatistics(common_stats=CommonStatistics(
                        num_non_missing=10
                    ))
                )])
        ]))

        self.assertEqual(len(datasets.datasets), 1)
        dataset = datasets.datasets[0]
        self.assertEqual(dataset.name, 'feature_name')
        self.assertEqual(len(dataset.features), 1)
        self.assertEqual(len(dataset.cross_features), 0)
        self.assertEqual(dataset.features[0].name, 'feature_name')

    def test_infer_dimensions_ok_multiple_features(self):
        datasets = infer_dimensions(DatasetFeatureStatisticsList(datasets=[
            DatasetFeatureStatistics(
                num_examples=10,
                features=[
                    FeatureNameStatistics(
                        name='feature_name1',
                        num_stats=NumericStatistics(
                            common_stats=CommonStatistics(
                                num_non_missing=10
                            ))
                    ),
                    FeatureNameStatistics(
                        name='feature_name2',
                        num_stats=NumericStatistics(
                            common_stats=CommonStatistics(
                                num_non_missing=10
                            ))
                    ),
                ]
                )]))

        self.assertEqual(len(datasets.datasets), 2)
        self.assertEqual(datasets.datasets[0].name, 'feature_name1')
        self.assertEqual(len(datasets.datasets[0].features), 1)
        self.assertEqual(len(datasets.datasets[0].cross_features), 0)
        self.assertEqual(datasets.datasets[1].name, 'feature_name2')
        self.assertEqual(len(datasets.datasets[1].features), 1)
        self.assertEqual(len(datasets.datasets[1].cross_features), 0)

    def test_infer_dimensions_ok_ignore_missing(self):
        datasets = infer_dimensions(DatasetFeatureStatisticsList(datasets=[
            DatasetFeatureStatistics(
                num_examples=1000,
                features=[
                    FeatureNameStatistics(
                        name='feature_name1',
                        num_stats=NumericStatistics(
                            common_stats=CommonStatistics(
                                num_non_missing=1
                            ))
                    ),
                    FeatureNameStatistics(
                        name='feature_name2',
                        num_stats=NumericStatistics(
                            common_stats=CommonStatistics(
                                num_non_missing=100
                            ))
                    ),
                ]
                )]))

        self.assertEqual(len(datasets.datasets), 1)
        self.assertEqual(datasets.datasets[0].name, 'feature_name2')
        self.assertEqual(len(datasets.datasets[0].features), 1)
        self.assertEqual(len(datasets.datasets[0].cross_features), 0)


if __name__ == '__main__':
    unittest.main()
