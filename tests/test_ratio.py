from dcstats.ratio import Ratio

def test_ratio():
    # Samples from treatment T1 and T2
    T1 = [2, 2, 2, 2, 2, 2]
    T2 = [1, 1, 1, 1, 1, 1]
    rt = Ratio(T1, T2)
    assert rt.ratio() == 2.0 