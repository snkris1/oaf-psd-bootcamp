import pytest
from is_prime import is_prime

def test_is_prime():
    # Test known primes
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(5) == True
    assert is_prime(7) == True
    assert is_prime(11) == True
    assert is_prime(13) == True
    
    # Test known non-primes
    assert is_prime(0) == False
    assert is_prime(1) == False
    assert is_prime(4) == False
    assert is_prime(6) == False
    assert is_prime(8) == False
    assert is_prime(9) == False
    assert is_prime(10) == False

    # Test larger primes
    assert is_prime(101) == True
    assert is_prime(103) == True
    assert is_prime(107) == True
    
    # Test larger non-primes
    assert is_prime(100) == False
    assert is_prime(102) == False
    assert is_prime(104) == False

if __name__ == "__main__":
    pytest.main()
