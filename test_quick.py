"""
Quick test script for US Map Plotter
Tests basic functionality without requiring browser display
"""

from us_map_plotter import USMapPlotter, quick_plot
import pandas as pd


def test_basic():
    """Test basic functionality"""
    print("Testing US Map Plotter...")
    print("-" * 50)

    # Test 1: Load from CSV
    print("\n✓ Test 1: Loading from CSV file")
    plotter = USMapPlotter('example_data.csv')
    print(f"  Loaded {len(plotter.plot_data)} states")

    # Test 2: Print statistics
    print("\n✓ Test 2: Getting statistics")
    stats = plotter.get_statistics()
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Min: {stats['min']:.2f}")
    print(f"  Max: {stats['max']:.2f}")

    # Test 3: Customization
    print("\n✓ Test 3: Customization")
    plotter.customize(
        title='Test Map',
        color_scheme='Blues',
        value_label='Sales'
    )
    print("  Successfully customized")

    # Test 4: Generate plot (don't show, just create)
    print("\n✓ Test 4: Generating map")
    fig = plotter.plot(save_as='test_output.html', show=False)
    print("  Map generated and saved to test_output.html")

    # Test 5: DataFrame input
    print("\n✓ Test 5: DataFrame input")
    df = pd.DataFrame({
        'state': ['CA', 'TX', 'FL', 'NY'],
        'value': [100, 200, 150, 180]
    })
    plotter2 = USMapPlotter(df)
    print(f"  Loaded {len(plotter2.plot_data)} states from DataFrame")

    # Test 6: Quick plot function
    print("\n✓ Test 6: Quick plot function")
    quick_plot('example_data.csv', title='Quick Test', save_as='test_quick_output.html')
    print("  Quick plot saved to test_quick_output.html")

    print("\n" + "="*50)
    print("All tests passed! ✅")
    print("="*50)
    print("\nGenerated files:")
    print("  - test_output.html")
    print("  - test_quick_output.html")
    print("\nOpen these files in a browser to view the maps.")


if __name__ == "__main__":
    test_basic()
