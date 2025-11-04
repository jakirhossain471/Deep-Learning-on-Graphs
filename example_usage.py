"""
Example Usage of US Map Plotter

This script demonstrates various ways to use the US Map Plotter
for creating professional visualizations.
"""

from us_map_plotter import USMapPlotter, quick_plot
import pandas as pd


def example_1_quick_plot():
    """Example 1: Simplest way to create a map"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Quick Plot")
    print("="*60)

    # Just one line!
    quick_plot(
        'example_data.csv',
        title='State Sales Data - Quick Plot',
        save_as='output_quick.html'
    )

    print("✓ Created: output_quick.html")


def example_2_basic_usage():
    """Example 2: Basic usage with customization"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Basic Usage")
    print("="*60)

    # Create plotter instance
    plotter = USMapPlotter('example_data.csv')

    # Print summary statistics
    plotter.print_summary()

    # Customize and plot
    plotter.customize(
        title='State Sales Performance 2024',
        color_scheme='Viridis',
        value_label='Sales ($)'
    )

    plotter.plot(save_as='output_basic.html', show=False)
    print("✓ Created: output_basic.html")


def example_3_from_dataframe():
    """Example 3: Using pandas DataFrame directly"""
    print("\n" + "="*60)
    print("EXAMPLE 3: From DataFrame")
    print("="*60)

    # Create DataFrame
    data = {
        'state_code': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL'],
        'revenue': [150000, 120000, 95000, 135000, 80000, 85000]
    }
    df = pd.DataFrame(data)

    # Create plot from DataFrame
    plotter = USMapPlotter(
        df,
        state_column='state_code',
        value_column='revenue'
    )

    plotter.customize(
        title='Top States by Revenue',
        color_scheme='RdYlGn',
        value_label='Revenue ($)'
    )

    plotter.plot(save_as='output_dataframe.html', show=False)
    print("✓ Created: output_dataframe.html")


def example_4_custom_colors():
    """Example 4: Different color schemes"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Color Schemes")
    print("="*60)

    color_schemes = {
        'Blues': 'Blues Theme',
        'Reds': 'Reds Theme',
        'Greens': 'Greens Theme',
        'Viridis': 'Viridis Theme',
        'Plasma': 'Plasma Theme',
        'RdYlGn': 'Red-Yellow-Green Diverging'
    }

    for scheme, description in list(color_schemes.items())[:3]:  # First 3 for demo
        plotter = USMapPlotter('example_data.csv')
        plotter.customize(
            title=f'Sales Data - {description}',
            color_scheme=scheme,
            value_label='Sales ($)'
        )
        filename = f'output_color_{scheme.lower()}.html'
        plotter.plot(save_as=filename, show=False)
        print(f"✓ Created: {filename}")


def example_5_different_styles():
    """Example 5: Different visual styles"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Different Styles")
    print("="*60)

    styles = ['professional', 'light', 'dark', 'colorblind']

    for style in styles:
        plotter = USMapPlotter('example_data.csv')
        plotter.customize(
            title=f'Sales Data - {style.capitalize()} Style',
            style=style,
            value_label='Sales ($)'
        )
        filename = f'output_style_{style}.html'
        plotter.plot(save_as=filename, show=False)
        print(f"✓ Created: {filename}")


def example_6_statistics():
    """Example 6: Getting statistics from data"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Data Statistics")
    print("="*60)

    plotter = USMapPlotter('example_data.csv')

    # Get statistics dictionary
    stats = plotter.get_statistics()

    print("\nDetailed Statistics:")
    print(f"  Total states with data: {stats['count']}")
    print(f"  Missing states: {stats['missing_states']}")
    print(f"  Average value: ${stats['mean']:,.2f}")
    print(f"  Median value: ${stats['median']:,.2f}")
    print(f"  Standard deviation: ${stats['std']:,.2f}")
    print(f"  Range: ${stats['min']:,.2f} - ${stats['max']:,.2f}")

    # Print formatted summary
    plotter.print_summary()


def example_7_export_data():
    """Example 7: Export processed data"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Export Processed Data")
    print("="*60)

    plotter = USMapPlotter('example_data.csv')

    # Export the processed data (includes full state names)
    plotter.export_data('processed_data.csv')

    print("✓ Processed data exported to: processed_data.csv")


def example_8_advanced_customization():
    """Example 8: Advanced customization options"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Advanced Customization")
    print("="*60)

    plotter = USMapPlotter('example_data.csv')

    # Advanced customization
    plotter.customize(
        title='Advanced Sales Visualization',
        color_scheme='RdBu',
        scale_type='linear',
        value_label='Sales Volume ($)',
        style='professional',
        width=1400,
        height=800,
        reverse_scale=False
    )

    plotter.plot(save_as='output_advanced.html', show=False)
    print("✓ Created: output_advanced.html")


def example_9_error_handling():
    """Example 9: Demonstrate error handling"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Error Handling")
    print("="*60)

    # Example with some invalid state codes
    data = {
        'state': ['CA', 'TX', 'ZZ', 'FL', 'XX', 'NY'],  # ZZ and XX are invalid
        'value': [100, 200, 150, 175, 225, 190]
    }
    df = pd.DataFrame(data)

    try:
        plotter = USMapPlotter(df)
        print("✓ Invalid state codes automatically filtered")
        print(f"✓ Valid states processed: {len(plotter.plot_data)}")
        plotter.plot(save_as='output_error_handling.html', show=False)
    except Exception as e:
        print(f"Error: {e}")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*70)
    print(" " * 15 + "US MAP PLOTTER - EXAMPLES")
    print("="*70)

    examples = [
        ("Quick Plot", example_1_quick_plot),
        ("Basic Usage", example_2_basic_usage),
        ("DataFrame Input", example_3_from_dataframe),
        ("Color Schemes", example_4_custom_colors),
        ("Visual Styles", example_5_different_styles),
        ("Statistics", example_6_statistics),
        ("Export Data", example_7_export_data),
        ("Advanced Options", example_8_advanced_customization),
        ("Error Handling", example_9_error_handling),
    ]

    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")

    print("\n" + "="*70)
    print("All examples completed!")
    print("Check the generated HTML files to view the interactive maps.")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Run individual examples or all
    run_all_examples()

    # Or run specific example:
    # example_1_quick_plot()
    # example_2_basic_usage()
    # etc.
