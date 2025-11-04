"""
Professional US States Map Data Plotter

A comprehensive tool for creating publication-quality and interactive choropleth maps
of US states with numerical data.

Author: Auto-generated
License: MIT
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Union, Optional, Dict, List, Tuple
import warnings
from pathlib import Path


# US State Abbreviations to Full Names Mapping
US_STATES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
}


class USMapPlotter:
    """
    Professional US States Map Plotter

    Creates interactive and static choropleth maps for US state-level data.

    Attributes:
        data (pd.DataFrame): The loaded and validated data
        state_column (str): Name of the state abbreviation column
        value_column (str): Name of the numerical value column
        config (dict): Configuration settings for the plot
    """

    def __init__(
        self,
        data_source: Union[str, pd.DataFrame],
        state_column: Optional[str] = None,
        value_column: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the US Map Plotter

        Args:
            data_source: Path to CSV/Excel file or pandas DataFrame
            state_column: Name of column containing state abbreviations (auto-detected if None)
            value_column: Name of column containing numerical values (auto-detected if None)
            **kwargs: Additional configuration options

        Raises:
            ValueError: If data cannot be loaded or validated
            FileNotFoundError: If file path doesn't exist
        """
        self.data = self._load_data(data_source)
        self.state_column = state_column or self._detect_state_column()
        self.value_column = value_column or self._detect_value_column()

        # Default configuration
        self.config = {
            'color_scheme': 'Blues',
            'scale_type': 'linear',  # 'linear', 'log', 'custom'
            'title': 'US States Data Visualization',
            'value_label': 'Value',
            'show_missing': True,
            'missing_color': '#E5E5E5',
            'style': 'professional',  # 'professional', 'light', 'dark', 'colorblind'
            'width': 1200,
            'height': 700,
            'reverse_scale': False,
            'custom_bins': None,
        }
        self.config.update(kwargs)

        # Validate and prepare data
        self._validate_data()
        self._prepare_data()

    def _load_data(self, data_source: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """Load data from various sources"""
        if isinstance(data_source, pd.DataFrame):
            return data_source.copy()

        path = Path(data_source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {data_source}")

        # Detect file type and load
        if path.suffix.lower() == '.csv':
            return pd.read_csv(data_source)
        elif path.suffix.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(data_source)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    def _detect_state_column(self) -> str:
        """Auto-detect the state abbreviation column"""
        for col in self.data.columns:
            # Check if column contains state abbreviations
            sample = self.data[col].dropna().astype(str).str.upper().head(20)
            if any(val in US_STATES for val in sample):
                return col

        # If not detected, assume first column
        return self.data.columns[0]

    def _detect_value_column(self) -> str:
        """Auto-detect the numerical value column"""
        for col in self.data.columns:
            if col != self.state_column and pd.api.types.is_numeric_dtype(self.data[col]):
                return col

        # If not detected, assume second column (or first non-state column)
        for col in self.data.columns:
            if col != self.state_column:
                return col

        raise ValueError("Could not detect value column")

    def _validate_data(self):
        """Validate the loaded data"""
        if self.data.empty:
            raise ValueError("Data is empty")

        if self.state_column not in self.data.columns:
            raise ValueError(f"State column '{self.state_column}' not found in data")

        if self.value_column not in self.data.columns:
            raise ValueError(f"Value column '{self.value_column}' not found in data")

        # Validate state codes
        invalid_states = []
        for state in self.data[self.state_column].dropna().astype(str).str.upper():
            if state and state not in US_STATES:
                invalid_states.append(state)

        if invalid_states:
            unique_invalid = list(set(invalid_states))
            warnings.warn(
                f"Invalid state codes found: {unique_invalid[:10]}... "
                f"({len(unique_invalid)} unique). These will be ignored."
            )

    def _prepare_data(self):
        """Prepare data for plotting"""
        # Create working copy
        df = self.data[[self.state_column, self.value_column]].copy()

        # Clean state codes
        df[self.state_column] = df[self.state_column].astype(str).str.upper().str.strip()

        # Filter valid states only
        df = df[df[self.state_column].isin(US_STATES.keys())]

        # Convert values to numeric
        df[self.value_column] = pd.to_numeric(df[self.value_column], errors='coerce')

        # Add full state names
        df['state_name'] = df[self.state_column].map(US_STATES)

        # Handle duplicates (keep first or average)
        df = df.groupby(self.state_column, as_index=False).agg({
            self.value_column: 'mean',
            'state_name': 'first'
        })

        self.plot_data = df

    def customize(
        self,
        color_scheme: Optional[str] = None,
        scale_type: Optional[str] = None,
        title: Optional[str] = None,
        value_label: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs
    ):
        """
        Customize plot appearance

        Args:
            color_scheme: Plotly color scale (e.g., 'Blues', 'Viridis', 'RdYlGn')
            scale_type: 'linear', 'log', or 'custom'
            title: Plot title
            value_label: Label for the value/color bar
            style: 'professional', 'light', 'dark', 'colorblind'
            **kwargs: Additional config options
        """
        if color_scheme:
            self.config['color_scheme'] = color_scheme
        if scale_type:
            self.config['scale_type'] = scale_type
        if title:
            self.config['title'] = title
        if value_label:
            self.config['value_label'] = value_label
        if style:
            self.config['style'] = style

        self.config.update(kwargs)
        return self

    def _get_color_scheme(self) -> str:
        """Get color scheme based on style"""
        style_schemes = {
            'professional': 'Blues',
            'light': 'Teal',
            'dark': 'Viridis',
            'colorblind': 'Cividis'
        }

        # Use custom color scheme if specified, otherwise use style default
        if self.config.get('color_scheme') and self.config['color_scheme'] not in style_schemes.values():
            return self.config['color_scheme']

        return style_schemes.get(self.config['style'], self.config['color_scheme'])

    def _apply_scale(self, values: np.ndarray) -> np.ndarray:
        """Apply scaling transformation to values"""
        if self.config['scale_type'] == 'log':
            # Handle negative and zero values for log scale
            min_val = values[values > 0].min() if (values > 0).any() else 1
            return np.log10(np.maximum(values, min_val))
        elif self.config['scale_type'] == 'custom' and self.config['custom_bins']:
            # Custom binning
            bins = self.config['custom_bins']
            return pd.cut(values, bins=bins, labels=False)
        else:
            return values

    def plot_interactive(
        self,
        title: Optional[str] = None,
        save_as: Optional[str] = None,
        show: bool = True
    ) -> go.Figure:
        """
        Create interactive Plotly choropleth map

        Args:
            title: Custom title (overrides config)
            save_as: Path to save HTML file
            show: Whether to display the plot

        Returns:
            plotly.graph_objects.Figure: The created figure
        """
        title = title or self.config['title']
        color_scheme = self._get_color_scheme()

        # Create the choropleth map
        fig = go.Figure(data=go.Choropleth(
            locations=self.plot_data[self.state_column],
            z=self.plot_data[self.value_column],
            locationmode='USA-states',
            colorscale=color_scheme,
            colorbar_title=self.config['value_label'],
            text=self.plot_data['state_name'],
            hovertemplate='<b>%{text}</b><br>' +
                         f"{self.config['value_label']}: " + '%{z:,.2f}<extra></extra>',
            reversescale=self.config['reverse_scale'],
        ))

        # Update layout
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'family': 'Arial, sans-serif'}
            },
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
            ),
            width=self.config['width'],
            height=self.config['height'],
            font=dict(family='Arial, sans-serif', size=12),
        )

        # Apply style-specific templates
        if self.config['style'] == 'dark':
            fig.update_layout(
                template='plotly_dark',
                geo=dict(bgcolor='#111111', lakecolor='#1f1f1f')
            )
        elif self.config['style'] in ['professional', 'light']:
            fig.update_layout(template='plotly_white')

        # Save if requested
        if save_as:
            save_path = Path(save_as)
            if save_path.suffix.lower() == '.html':
                fig.write_html(save_as)
                print(f"✓ Interactive map saved to: {save_as}")
            elif save_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.svg', '.pdf']:
                fig.write_image(save_as)
                print(f"✓ Static image saved to: {save_as}")
            else:
                fig.write_html(save_as + '.html')
                print(f"✓ Interactive map saved to: {save_as}.html")

        # Show if requested
        if show:
            fig.show()

        return fig

    def plot(
        self,
        interactive: bool = True,
        title: Optional[str] = None,
        save_as: Optional[str] = None,
        show: bool = True
    ) -> go.Figure:
        """
        Create map plot (wrapper method)

        Args:
            interactive: Create interactive plotly map (True) or static (False)
            title: Custom title
            save_as: Path to save the plot
            show: Whether to display the plot

        Returns:
            The created figure
        """
        if interactive:
            return self.plot_interactive(title=title, save_as=save_as, show=show)
        else:
            return self.plot_interactive(title=title, save_as=save_as, show=show)

    def get_statistics(self) -> Dict:
        """
        Get statistical summary of the data

        Returns:
            Dictionary containing statistics
        """
        values = self.plot_data[self.value_column]

        stats = {
            'count': len(values),
            'mean': values.mean(),
            'median': values.median(),
            'std': values.std(),
            'min': values.min(),
            'max': values.max(),
            'missing_states': len(US_STATES) - len(values),
            'total_states': len(US_STATES)
        }

        return stats

    def print_summary(self):
        """Print a summary of the data and statistics"""
        stats = self.get_statistics()

        print("\n" + "="*60)
        print("US MAP DATA SUMMARY")
        print("="*60)
        print(f"States with data: {stats['count']}/{stats['total_states']}")
        print(f"Missing states: {stats['missing_states']}")
        print(f"\n{self.config['value_label']} Statistics:")
        print(f"  Mean:   {stats['mean']:,.2f}")
        print(f"  Median: {stats['median']:,.2f}")
        print(f"  Std:    {stats['std']:,.2f}")
        print(f"  Min:    {stats['min']:,.2f}")
        print(f"  Max:    {stats['max']:,.2f}")
        print("="*60 + "\n")

    def export_data(self, filepath: str):
        """
        Export processed data to CSV

        Args:
            filepath: Path to save the CSV file
        """
        self.plot_data.to_csv(filepath, index=False)
        print(f"✓ Data exported to: {filepath}")


# Convenience function for quick plotting
def quick_plot(
    data_source: Union[str, pd.DataFrame],
    title: str = "US States Data Visualization",
    color_scheme: str = "Blues",
    save_as: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """
    Quick plot function for simple use cases

    Args:
        data_source: Path to data file or DataFrame
        title: Plot title
        color_scheme: Color scheme name
        save_as: Path to save the plot
        **kwargs: Additional configuration

    Returns:
        The created figure

    Example:
        >>> quick_plot('state_data.csv', title='Sales by State', save_as='map.html')
    """
    plotter = USMapPlotter(data_source, **kwargs)
    plotter.customize(title=title, color_scheme=color_scheme)
    return plotter.plot(save_as=save_as)


if __name__ == "__main__":
    # Example usage
    print("""
    US Map Plotter - Professional Grade Visualization Tool

    Quick Start:
    ------------
    from us_map_plotter import USMapPlotter, quick_plot

    # Method 1: Quick plot
    quick_plot('your_data.csv', title='My Map', save_as='output.html')

    # Method 2: Advanced usage
    plotter = USMapPlotter('your_data.csv')
    plotter.customize(
        color_scheme='Viridis',
        title='Advanced Map',
        style='professional'
    )
    plotter.print_summary()
    plotter.plot(save_as='output.html')

    See example_usage.py for more examples.
    """)
