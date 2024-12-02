import ternary
import pandas as pd
import numpy as np

# Set parameters for displaying the ternary diagram
scale = 100
interval = scale/10
fig, tax = ternary.figure(scale=scale)
tax.boundary(linewidth=1.0)
tax.gridlines(color="black", multiple=interval)

# Set title, corner labels, and axis labels of the ternary diagram
tax.set_title("Ternary Phase Diagram of Water-1-Butanol-Acetone Solvent System\n\n")
tax.right_corner_label("Water")
tax.top_corner_label("Acetone")
tax.left_corner_label("1-Butanol")
tax.left_axis_label("%v A-B Binary\n")
tax.right_axis_label("%v A-W Binary\n")
tax.bottom_axis_label("%v B-W Binary\n")

# Read all points required for the ternary diagram
BinodalCurve_DF = pd.read_csv('TPDV_Binodal_Curve_Points.csv')
TieLines_DF = pd.read_csv('TPDV_Tie_Line_Points.csv')
ConjCurvePP_DF = pd.read_csv('TPDV_ConjCurve_and_PlaitPoint_Points.csv')

# Read data frame containing the coefficients of the binodal and conjugate curves
# Binodal Curve Equation:    y = Ax⁵ + Bx⁴ + Cx³ + Dx² + Ex + F
# Conjugate Curve Equation:  y = A + Bx + Cx²
CoefficientsBinodalCurve_DF = pd.read_csv('TPDV_Binodal_Curve_Polynomial_Coefficients.csv')
CoefficientsConjCurve_DF = pd.read_csv('TPDV_ConjCurve_Polynomial_Coefficients.csv')

# Adjust the way data frames are displayed when printed
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

# Sort rows of the data frame for Binodal Curve
BinodalCurve_DF = BinodalCurve_DF.sort_values(by=['v% Water'])

# Get the points required for the ternary diagram
BinodalCurve_Points = [tuple(np.array(list(i)[1:])*100) for i in BinodalCurve_DF.iloc[:, 1:].itertuples()]
TieLine1_Points = [tuple(np.array(list(i)[1:])*100) for i in TieLines_DF.iloc[0:3, 2:].itertuples()]
TieLine2_Points = [tuple(np.array(list(i)[1:])*100) for i in TieLines_DF.iloc[3:6, 2:].itertuples()]
TieLine3_Points = [tuple(np.array(list(i)[1:])*100) for i in TieLines_DF.iloc[6:9, 2:].itertuples()]
ConjCurve_Points = [tuple(np.array(list(i)[1:])*100) for i in ConjCurvePP_DF.iloc[0:3, 1:].itertuples()]
PlaitPoint = tuple(np.array(list(ConjCurvePP_DF.iloc[3, 1:]))*100)
PlaitPoint_Points = []
PlaitPoint_Points.append(PlaitPoint)

# Set colors for the plot
colors = ["#4472C4", # blue color for the binodal curve
          "#ED7D31", # orange color for tie line #1
          "#A5A5A5", # silver color for tie line #2
          "#FEC001", # gold color for tie line #3
          "green", # green color for conjugate curve
          "black"]  # black color for the plait point

# Plot the scatter points for binodal curve, all tie lines, conjugate curve, and plait point:
SeriesNames = ["Binodal Curve",
               "Tie Line #1",
               "Tie Line #2",
               "Tie Line #3",
               "Conjugate Curve",
               "Plait Point"]
SeriesPoints = [BinodalCurve_Points,
                TieLine1_Points,
                TieLine2_Points,
                TieLine3_Points,
                ConjCurve_Points,
                PlaitPoint_Points]
SeriesMarkers = ['*',
                 '*',
                 '*',
                 '*',
                 'o',
                 'D']
for name, color, ternary_points, marker in zip(SeriesNames, colors, SeriesPoints, SeriesMarkers):
    tax.scatter(ternary_points, color=color, label=name, marker=marker, zorder=2)
tax.legend()

# Compute points required for plotting the binodal curve:
vectorCoefficients_Binodal = np.array(list(CoefficientsBinodalCurve_DF.iloc[:, 1]))
rangeVolFracWater_Binodal = np.linspace(0, 1, 400, endpoint=True)
BinodalCurvePolynomial_Points = []
for volFracWater in rangeVolFracWater_Binodal:
    powersVolFracWater = np.power(np.full(6, volFracWater), np.array([5, 4, 3, 2, 1, 0]))
    volFracAcetone = np.dot(vectorCoefficients_Binodal, powersVolFracWater)
    if volFracAcetone < 0:
        continue
    volFracButanol = 1 - volFracWater - volFracAcetone
    ternaryPoint = tuple(np.array([volFracWater, volFracAcetone, volFracButanol])*100)
    BinodalCurvePolynomial_Points.append(ternaryPoint)

# Compute points required for plotting the conjugate curve:
vectorCoefficients_Conj = np.array(list(CoefficientsConjCurve_DF.iloc[:, 1]))
rangeVolFracWater_Conj = np.linspace(ConjCurve_Points[2][0]/100, PlaitPoint_Points[0][0]/100, 400, endpoint=True)
ConjCurvePolynomial_Points = []
for volFracWater in rangeVolFracWater_Conj:
    powersVolFracWater = np.power(np.full(3, volFracWater), np.array([0, 1, 2]))
    volFracAcetone = np.dot(vectorCoefficients_Conj, powersVolFracWater)
    volFracButanol = 1 - volFracWater - volFracAcetone
    ternaryPoint = tuple(np.array([volFracWater, volFracAcetone, volFracButanol]) * 100)
    ConjCurvePolynomial_Points.append(ternaryPoint)

# Plot the binodal, conjugate curves, and tie lines
CurvePoints = [BinodalCurvePolynomial_Points,
               ConjCurvePolynomial_Points,
               TieLine1_Points,
               TieLine2_Points,
               TieLine3_Points,]
colorsCurve = ["#4472C4",  # blue color for the binodal curve
               "green",    # black color for conjugate curve
               "#ED7D31",  # orange color for tie line #1
               "#A5A5A5",  # silver color for tie line #2
               "#FEC001"]  # gold color for tie line #3
lineStyles = ["solid",  # solid line for binodal curve
              "dashed", # dashed line for conjugate curve
              "dotted", # dotted line for tie line #1
              "dotted", # dotted line for tie line #2
              "dotted"] # dotted line for tie line #3
for color, style, ternaryPoints in zip(colorsCurve, lineStyles, CurvePoints):
    tax.plot(ternaryPoints, linewidth=2.0, color=color, linestyle=style, zorder=1)

# Finalize and show the ternary phase diagram
tax.ticks(axis="lbr", multiple=interval, linewidth=2, clockwise=False)
tax.get_axes().axis('off')
tax.clear_matplotlib_ticks()
tax.show()

