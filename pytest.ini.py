[pytest]
addopt= --reruns 2 --reruns-delay 5 -n auto
markers=
    data_extraction: data extraction checks
    data_quality: data quality checks
    data_loading: data loading checks
    data_transformation: data transformation checks
    schema_validation: schema validation checks
    regression: regression checks
    smoke: smoke checks