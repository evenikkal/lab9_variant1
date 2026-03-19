use pyo3::prelude::*;

fn sum_squares_impl(numbers: &[i64]) -> i64 {
    numbers.iter().map(|x| x * x).sum()
}

#[pyfunction]
fn sum_squares(numbers: Vec<i64>) -> i64 {
    sum_squares_impl(&numbers)
}

#[pymodule]
fn fastmath(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_squares, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sum_squares_basic() {
        assert_eq!(sum_squares_impl(&[1, 2, 3, 4, 5]), 55);
    }

    #[test]
    fn test_sum_squares_empty() {
        assert_eq!(sum_squares_impl(&[]), 0);
    }

    #[test]
    fn test_sum_squares_single() {
        assert_eq!(sum_squares_impl(&[7]), 49);
    }

    #[test]
    fn test_sum_squares_negative() {
        assert_eq!(sum_squares_impl(&[-3, -4]), 25);
    }
}