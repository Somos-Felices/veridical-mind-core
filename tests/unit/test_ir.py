from src.mrec.ir import calculate_ir, rank_results

def test_ir():
    assert calculate_ir(1.0, 0.8) == 0.8
    assert calculate_ir(0.5, 0.8) == 0.4
    assert calculate_ir(0.0, 0.9) == 0.0

def test_rank_results():
    results = [
        {
            "id": "1",
            "content": "A",
            "source_doc": "doc1",
            "source_type": "primary",
            "icd": 0.5,
            "similarity": 0.9,
        },
        {
            "id": "2",
            "content": "B",
            "source_doc": "doc2",
            "source_type": "secondary",
            "icd": 1.0,
            "similarity": 0.7,
        },
    ]

    ranked = rank_results(results)

    assert ranked[0].id == "2"
    assert ranked[0].ir == 0.7
