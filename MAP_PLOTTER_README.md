# US States Map Data Plotter

A professional-grade Python tool for creating beautiful, interactive choropleth maps of US state-level data.

## Features

✨ **Easy to Use**
- Simple one-line quick plot function
- Auto-detection of state and value columns
- Supports CSV, Excel, and pandas DataFrames

🎨 **Professional Visualizations**
- Interactive HTML maps with hover tooltips
- Multiple color schemes (Blues, Viridis, RdYlGn, etc.)
- Customizable styles (professional, light, dark, colorblind-friendly)
- Publication-quality output

📊 **Data Intelligence**
- Automatic data validation
- Invalid state code filtering
- Duplicate handling
- Missing data visualization
- Statistical summaries

💪 **Robust & Flexible**
- Type hints for better IDE support
- Comprehensive error handling
- Export to HTML, PNG, SVG, PDF
- Configurable dimensions and scales

---

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas numpy plotly openpyxl kaleido
```

### 2. Download the Script

Save `us_map_plotter.py` to your project directory.

---

## Quick Start

### Simplest Usage (One Line!)

```python
from us_map_plotter import quick_plot

quick_plot('your_data.csv', title='My Map', save_as='output.html')
```

### Basic Usage

```python
from us_map_plotter import USMapPlotter

# Create plotter
plotter = USMapPlotter('your_data.csv')

# Customize
plotter.customize(
    title='State Sales Data',
    color_scheme='Blues',
    value_label='Sales ($)'
)

# Generate map
plotter.plot(save_as='map.html')
```

---

## Data Format

Your data should have **two columns**:

| Column 1: State Code | Column 2: Numerical Value |
|----------------------|---------------------------|
| CA                   | 125000                    |
| TX                   | 98500                     |
| FL                   | 87200                     |
| NY                   | 112000                    |
| ...                  | ...                       |

**Supported Formats:**
- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`)
- Pandas DataFrames

**State Codes:** Use standard 2-letter abbreviations (CA, TX, FL, NY, etc.)

### Example Data File (example_data.csv)

```csv
state,sales
CA,125000
TX,98500
FL,87200
NY,112000
```

---

## Usage Examples

### Example 1: From CSV File

```python
from us_map_plotter import USMapPlotter

plotter = USMapPlotter('sales_data.csv')
plotter.customize(title='State Sales 2024')
plotter.plot(save_as='sales_map.html')
```

### Example 2: From DataFrame

```python
import pandas as pd
from us_map_plotter import USMapPlotter

# Your data
df = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY'],
    'revenue': [150000, 120000, 95000, 135000]
})

plotter = USMapPlotter(df, state_column='state', value_column='revenue')
plotter.plot(save_as='revenue_map.html')
```

### Example 3: Custom Styling

```python
plotter = USMapPlotter('data.csv')

plotter.customize(
    title='Sales Performance Map',
    color_scheme='Viridis',      # Color palette
    style='professional',         # Visual style
    value_label='Revenue ($)',    # Legend label
    width=1400,                   # Custom width
    height=800                    # Custom height
)

plotter.plot(save_as='custom_map.html')
```

### Example 4: Get Statistics

```python
plotter = USMapPlotter('data.csv')

# Print formatted summary
plotter.print_summary()

# Get statistics dictionary
stats = plotter.get_statistics()
print(f"Mean: ${stats['mean']:,.2f}")
print(f"States covered: {stats['count']}/{stats['total_states']}")
```

### Example 5: Export Data

```python
plotter = USMapPlotter('data.csv')

# Export processed data (includes full state names)
plotter.export_data('processed_output.csv')
```

---

## Customization Options

### Color Schemes

Available Plotly color scales:

**Sequential:**
- `'Blues'` - Blue gradient (default)
- `'Greens'` - Green gradient
- `'Reds'` - Red gradient
- `'Viridis'` - Perceptually uniform
- `'Plasma'` - Vibrant plasma colors
- `'Cividis'` - Colorblind-friendly

**Diverging:**
- `'RdBu'` - Red-Blue diverging
- `'RdYlGn'` - Red-Yellow-Green
- `'Spectral'` - Full spectrum

[See all Plotly color scales](https://plotly.com/python/builtin-colorscales/)

### Styles

- `'professional'` - Clean, publication-ready (default)
- `'light'` - Light theme with soft colors
- `'dark'` - Dark background theme
- `'colorblind'` - Optimized for colorblind users

### Scale Types

- `'linear'` - Linear scale (default)
- `'log'` - Logarithmic scale
- `'custom'` - Custom binning

---

## API Reference

### Class: `USMapPlotter`

#### Constructor

```python
USMapPlotter(
    data_source: Union[str, pd.DataFrame],
    state_column: Optional[str] = None,
    value_column: Optional[str] = None,
    **kwargs
)
```

**Parameters:**
- `data_source`: Path to CSV/Excel file or pandas DataFrame
- `state_column`: Name of state abbreviation column (auto-detected if None)
- `value_column`: Name of numerical value column (auto-detected if None)
- `**kwargs`: Additional configuration options

#### Methods

##### `customize(**kwargs)`

Customize plot appearance.

```python
plotter.customize(
    color_scheme='Blues',
    scale_type='linear',
    title='My Map',
    value_label='Value',
    style='professional',
    width=1200,
    height=700,
    reverse_scale=False
)
```

##### `plot(interactive=True, title=None, save_as=None, show=True)`

Create and display the map.

**Parameters:**
- `interactive`: Create interactive HTML map (default: True)
- `title`: Custom title (overrides config)
- `save_as`: Path to save file (HTML, PNG, SVG, PDF)
- `show`: Whether to display the plot (default: True)

**Returns:** Plotly Figure object

##### `print_summary()`

Print formatted data summary and statistics.

##### `get_statistics()`

Get statistical summary as dictionary.

**Returns:** Dict with keys: `count`, `mean`, `median`, `std`, `min`, `max`, `missing_states`, `total_states`

##### `export_data(filepath)`

Export processed data to CSV.

---

### Function: `quick_plot()`

Convenience function for quick plotting.

```python
quick_plot(
    data_source: Union[str, pd.DataFrame],
    title: str = "US States Data Visualization",
    color_scheme: str = "Blues",
    save_as: Optional[str] = None,
    **kwargs
)
```

---

## Advanced Usage

### Method Chaining

```python
(USMapPlotter('data.csv')
    .customize(title='Chained Plot', color_scheme='Viridis')
    .plot(save_as='output.html', show=False))
```

### Multiple Exports

```python
plotter = USMapPlotter('data.csv')
plotter.customize(title='Multi-Export Map')

# Export to multiple formats
fig = plotter.plot(save_as='map.html', show=False)
fig.write_image('map.png')
fig.write_image('map.pdf')
```

### Custom Configuration

```python
plotter = USMapPlotter(
    'data.csv',
    color_scheme='Plasma',
    scale_type='log',
    width=1600,
    height=900,
    show_missing=True,
    missing_color='#CCCCCC'
)
```

---

## Running the Examples

The package includes a comprehensive example script:

```bash
python example_usage.py
```

This will generate multiple example maps demonstrating different features:
- `output_quick.html` - Quick plot example
- `output_basic.html` - Basic usage
- `output_dataframe.html` - DataFrame input
- `output_color_*.html` - Different color schemes
- `output_style_*.html` - Different styles
- `output_advanced.html` - Advanced customization

---

## Supported US States

All 50 states plus DC (51 total):

```
AL, AK, AZ, AR, CA, CO, CT, DE, FL, GA, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD,
MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PA, RI, SC,
SD, TN, TX, UT, VT, VA, WA, WV, WI, WY, DC
```

---

## Troubleshooting

### Issue: Module not found

```bash
pip install pandas numpy plotly
```

### Issue: Can't save PNG/PDF images

Install kaleido:
```bash
pip install kaleido
```

### Issue: Can't read Excel files

Install openpyxl:
```bash
pip install openpyxl
```

### Issue: Invalid state codes warning

The plotter automatically filters invalid state codes. Check your data for typos in state abbreviations.

### Issue: Map not showing

Make sure to either:
- Set `show=True` in `plot()` method, OR
- Open the saved HTML file in a web browser

---

## Performance Tips

- **Large datasets**: Use `show=False` and save to HTML for better performance
- **Multiple maps**: Reuse the same USMapPlotter instance with different customizations
- **Static images**: PNG/PDF export requires kaleido and may be slower than HTML

---

## Best Practices

1. **Data Validation**: Always check your data has valid state codes
2. **Color Choice**: Use colorblind-friendly schemes for accessibility
3. **Titles**: Use descriptive titles that explain what the data represents
4. **Scale**: Use log scale for data with large value ranges
5. **Export**: Use HTML for interactivity, PNG/PDF for publications

---

## Examples of Use Cases

- **Sales Analysis**: Visualize sales performance by state
- **Demographics**: Display population, income, or census data
- **Elections**: Show voting patterns and results
- **Public Health**: Map disease rates or health metrics
- **Economics**: Visualize GDP, unemployment, or economic indicators
- **Education**: Display test scores or graduation rates
- **Real Estate**: Show housing prices or market trends

---

## Technical Details

**Dependencies:**
- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.20.0
- plotly >= 5.0.0
- openpyxl >= 3.0.0 (optional, for Excel)
- kaleido >= 0.2.1 (optional, for image export)

**Output Formats:**
- HTML (interactive)
- PNG (static image)
- SVG (vector graphics)
- PDF (printable)

---

## License

MIT License - Free to use for personal and commercial projects.

---

## Support & Contribution

Found a bug? Have a feature request?

Please ensure your data follows the two-column format (state codes + numerical values) for best results.

---

## Changelog

### Version 1.0 (2024)
- Initial release
- Interactive choropleth maps
- Multiple color schemes and styles
- Auto-detection of columns
- Data validation and statistics
- Export to multiple formats
- Comprehensive examples

---

**Happy Mapping! 🗺️**
