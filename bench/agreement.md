# Label disagreements (Claude accepted, Gemini blind label said not relevant)

30 of 48 accepted papers: both agree relevant. The 18 below were decided against the code itself with one rule: keep a paper if it is the original of a method the code uses, addresses the problem the code actually solves, or evaluates the exact tool the code uses; drop it if it is a technique the code does not use or a setting with nothing that transfers.

Result: 9 keep, 9 drop. Precision of the accepted list: (30 + 9) / 48 = **0.81**. Gemini alone: 0.63. Claude alone: 1.00 (by construction, so not a measure). Of the 9 drops, 6 are alternative techniques or other platforms for the same task (hand trackers, Unity ports), and 3 share a surface idea but not the setting. The main cause of false accepts is that the judge rubric rewards same-task papers even when the technique is not used.

## A. Original paper of a library the code uses (XGBoost, LightGBM, Kelly 1956)

| # | Paper | Claude's reason | Gemini's reason | Decision |
|---|---|---|---|---|
| 9 | LightGBM: A Highly Efficient Gradient Boosting Decision Tree (trading engine) | Seed: LightGBM, the classifier built in core/models.py:246. | Focuses on internal GBDT split-finding optimizations rather than financial triple-barrier meta-labeling.  | **keep**: foundation: LGBMClassifier is built in core/models.py |
| 29 | XGBoost (trading engine) | Seed: XGBoost, the classifier built in core/models.py:317. | Covers internal distributed systems engineering of XGBoost rather than financial triple-barrier meta-labeling.  | **keep**: foundation: XGBClassifier is built in core/models.py |
| 37 | A New Interpretation of Information Rate (trading engine) | Seed: Kelly's original paper behind _calculate_kelly_size. | Derives theoretical channel-capacity gambling growth rates without addressing fractional sizing or drawdown control.  | **keep**: foundation: engine.py:345 is Kelly's formula k=(p*b-(1-p))/b |

## B. Gemini looks right: different problem or setting

| # | Paper | Claude's reason | Gemini's reason | Decision |
|---|---|---|---|---|
| 10 | Real-time hand tracking visualization using media pipe and touch designer (air-canvas) | MediaPipe hand landmarks from a webcam. | Streams MediaPipe keypoints over OSC to TouchDesigner for visuals rather than informing browser landmark tracking.  | **drop**: integration with TouchDesigner; no technique the app can use; unvetted venue |
| 16 | New Evidence on Mutual Fund Performance: A Comparison of Alternative Bootstrap Methods (trading engine) | Bootstrap inference on manager returns. | Compares cross-sectional panel bootstraps across mutual fund managers rather than time-series block bootstrap of strategy returns.  | **drop**: cross-sectional luck-vs-skill over many funds; code bootstraps one strategy by weekly blocks |
| 22 | Hand Gesture Recognition and Volume Control (air-canvas) | Rule on thumb-index landmark distance, like the pinch rules in the app. | Maps thumb-index distance solely to OS audio volume via Pycaw rather than mid-air drawing gestures.  | **drop**: continuous thumb-index distance for volume; nothing beyond the app's own pinch rule |
| 23 | Parsimonious Optimization of Multitask Neural Network Hyperparameters (trading engine) | Compares TPE with other search methods. | Benchmarks standard HPO methods on chemical QSAR neural networks without algorithmic insights for noisy backtest TPE.  | **drop**: TPE vs grid/GA on chemistry networks; a domain-specific benchmark does not transfer |
| 43 | Greeks-Aware Profitability Labeling for Intraday Nifty 50 Options Trading Using Hybrid Mac (trading engine) | Profitability-based labeling of intraday bars for ML classifiers. | Labels intraday options using Black-Scholes Greeks and implied volatility shocks rather than spot triple-barrier thresholds.  | **drop**: shares the profit-based label idea, but the content (Greeks, implied volatility) does not apply to spot gold |
| 45 | A Study on the Classification of Hand Gesture for Mobile Virtual Reality with MediaPipe (air-canvas) | Gesture classification with MediaPipe hand tracking. | Benchmarks Unity Barracuda, TFLite, and C# MediaPipe ports for mobile VR games rather than browser tracking.  | **drop**: Unity/C# ports for VR; the app runs MediaPipe JS in a browser |

## C. Same task, different technique or angle (judgment call)

| # | Paper | Claude's reason | Gemini's reason | Decision |
|---|---|---|---|---|
| 1 | Twenty-one degrees of freedom model based hand pose tracking using a monocular RGB camera (air-canvas) | Real-time hand tracking from one RGB camera. | Uses a custom piecewise-planar 3D hand model on CPU rather than MediaPipe Hands landmark regression.  | **drop**: alternative model-based tracker the app does not use |
| 7 | A Bayesian Approach to Backtest Overfitting (trading engine) | Bayesian estimate of backtest overfitting. | Proposes MCMC Bayesian multiple-testing adjustments on static holdouts rather than purged walk-forward validation.  | **keep**: same problem: gauntlet.py computes DSR over the optimizer's n_trials (multiple testing) |
| 11 | Real-Time 3D Hand-Object Pose Estimation for Mobile Devices (air-canvas) | Hand pose estimation on mobile without depth sensors. | Proposes a custom mobile 3D hand-object pose network rather than MediaPipe Hands webcam tracking.  | **drop**: 3D hand-object network; the app uses 2D landmarks and no objects |
| 14 | Statistical Overfitting and Backtest Performance (trading engine) | Explains in-sample overfitting of strategy parameters. | Describes a pedagogical random-walk web simulator demonstrating overfitting rather than a walk-forward validation method.  | **keep**: same problem as 7; teaching tool, no new method |
| 18 | Extreme Value Theory and Backtest Overfitting in Finance (trading engine) | Backtest overfitting under many configurations. | Uses Extreme Value Theory for multiple-testing bounds rather than walk-forward validation or purged chronological folds.  | **keep**: same problem as 7; weak source (undergraduate thesis) |
| 24 | FastHand: Fast Hand Pose Estimation From A Monocular Camera. (air-canvas) | Fast landmark prediction from a monocular camera. | Introduces a custom encoder-decoder CNN for Jetson GPUs rather than MediaPipe Hands browser tracking.  | **drop**: alternative CNN tracker on Jetson; not used |
| 30 | PSEUDO MATHEMATICS AND FINANCIAL CHARLATANISM: BACKTEST OVERFITTING AND OUT-OF-SAMPLE PERF (trading engine) | Backtest overfitting from many configurations, relevant to the optimizer search. | Truncated high-level critique of backtest overfitting lacking concrete walk-forward or purging methodology.  | **keep**: same problem as 7, by the DSR authors the code cites |
| 31 | AI Based Real-Time Air Gesture Recognition & Drawing System (air-canvas) | Mid-air drawing from a standard webcam. | Classifies finished doodles using TensorFlow QuickDraw rather than rule-based hand landmark gesture tracking.  | **keep**: same task: mid-air drawing from a webcam |
| 39 | Hand tracking for clinical applications: Validation of the Google MediaPipe Hand (GMH) and (air-canvas) | Accuracy check of the MediaPipe hand tracker the app relies on. | Validates MediaPipe Hand and RGB-D variants against motion capture for clinical rehabilitation assessment.  | **keep**: measures the accuracy of the exact tracker the app uses (MediaPipe Hands) |
