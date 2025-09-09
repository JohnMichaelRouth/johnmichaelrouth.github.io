#!/usr/bin/env python3
"""
Test script to verify the distribution functions work correctly
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import os

def generate_delay(min_delay=20, max_delay=80, target=50, deviation=5, weighted=False):
    """Generate a delay value based on the current distribution settings"""
    if weighted:
        # Log-normal distribution (right-shifted)
        mu = math.log(target)
        sigma = deviation / target  # Relative deviation
        delay = np.random.lognormal(mu, sigma)
    else:
        # Normal gaussian distribution
        delay = np.random.normal(target, deviation)
    
    # Clamp to absolute bounds
    delay = max(min_delay, min(max_delay, delay))
    return delay

def test_distributions():
    """Test both distribution types and generate sample data"""
    print("Testing Distribution Functions")
    print("=" * 40)
    
    # Parameters
    min_delay = 20
    max_delay = 80
    target = 50
    deviation = 5
    sample_size = 10000
    
    print(f"Parameters: min={min_delay}, max={max_delay}, target={target}, deviation={deviation}")
    print(f"Sample size: {sample_size}")
    print()
    
    # Test standard distribution
    print("Testing Standard (Gaussian) Distribution:")
    standard_samples = [generate_delay(min_delay, max_delay, target, deviation, False) for _ in range(sample_size)]
    
    print(f"  Mean: {np.mean(standard_samples):.2f}")
    print(f"  Median: {np.median(standard_samples):.2f}")
    print(f"  Std Dev: {np.std(standard_samples):.2f}")
    print(f"  Min: {np.min(standard_samples):.2f}")
    print(f"  Max: {np.max(standard_samples):.2f}")
    print()
    
    # Test weighted distribution
    print("Testing Weighted (Log-Normal) Distribution:")
    weighted_samples = [generate_delay(min_delay, max_delay, target, deviation, True) for _ in range(sample_size)]
    
    print(f"  Mean: {np.mean(weighted_samples):.2f}")
    print(f"  Median: {np.median(weighted_samples):.2f}")
    print(f"  Std Dev: {np.std(weighted_samples):.2f}")
    print(f"  Min: {np.min(weighted_samples):.2f}")
    print(f"  Max: {np.max(weighted_samples):.2f}")
    print()
    
    # Show some sample values
    print("Sample delays from each distribution:")
    print("Standard:", [round(x, 1) for x in standard_samples[:10]])
    print("Weighted:", [round(x, 1) for x in weighted_samples[:10]])
    print()
    
    # Try to create a simple histogram plot
    try:
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.hist(standard_samples, bins=50, alpha=0.7, color='green', label='Standard (Gaussian)')
        plt.title('Standard Distribution')
        plt.xlabel('Delay (ms)')
        plt.ylabel('Frequency')
        plt.axvline(target, color='red', linestyle='--', label=f'Target ({target})')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.hist(weighted_samples, bins=50, alpha=0.7, color='blue', label='Weighted (Log-Normal)')
        plt.title('Weighted Distribution')
        plt.xlabel('Delay (ms)')
        plt.ylabel('Frequency')
        plt.axvline(target, color='red', linestyle='--', label=f'Target ({target})')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('/tmp/distribution_comparison.png', dpi=150, bbox_inches='tight')
        print("Distribution comparison saved to /tmp/distribution_comparison.png")
        
    except ImportError:
        print("Matplotlib not available, skipping plot generation")
        print("Install with: pip install matplotlib")
    
    return standard_samples, weighted_samples

if __name__ == "__main__":
    test_distributions()