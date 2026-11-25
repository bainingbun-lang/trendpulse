from trendpulse import parse_traffic


def test_thousands():
    assert parse_traffic("200K+") == 200000


def test_millions():
    assert parse_traffic("1.5M+") == 1500000


def test_plain_number():
    assert parse_traffic("500") == 500


def test_garbage():
    assert parse_traffic("") == 0


if __name__ == "__main__":
    test_thousands()
    test_millions()
    test_plain_number()
    test_garbage()
    print("ok")
