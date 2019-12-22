package com.example.location.impl.ble.ibeacon.transfomers;


import org.apache.commons.math3.fitting.leastsquares.LeastSquaresBuilder;
import org.apache.commons.math3.fitting.leastsquares.LeastSquaresOptimizer;
import org.apache.commons.math3.fitting.leastsquares.LeastSquaresProblem;
import org.apache.commons.math3.fitting.leastsquares.LevenbergMarquardtOptimizer;
import org.apache.commons.math3.fitting.leastsquares.MultivariateJacobianFunction;
import org.apache.commons.math3.linear.Array2DRowRealMatrix;
import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.RealVector;
import org.apache.commons.math3.util.Pair;

import java.util.List;

import static com.google.common.primitives.Doubles.toArray;
import static java.lang.StrictMath.log;
import static java.lang.StrictMath.log10;
import static java.lang.StrictMath.pow;

/**
 * Runs an optimization problem considering the base power and the coefficient as variables.
 */
public class CoeffAndBasePowerOptimizationBasedValueResolver implements OptimizationBasedValueResolver{

    private static final double PWR_SEED = -80.0;
    private static final double COEFF_SEED = 0.5;
    private static final int MAX_ITERATIONS = 1000;
    private static final int MAX_EVALUATIONS = 1000;
    private static final LeastSquaresOptimizer OPTIMIZER = new LevenbergMarquardtOptimizer();

    private double mediumCoeff;
    private double basePower;

    private LeastSquaresProblem problem;

    public static OptimizationBasedValueResolverFactory coeffAndBasePowerValueResolver() {
        return (d,p,s) -> new CoeffAndBasePowerOptimizationBasedValueResolver(d,p);
    }

    private CoeffAndBasePowerOptimizationBasedValueResolver(List<Double> realDistances, List<Double> measuredPowers) {
        this.problem = createProblem(measuredPowers, realDistances);
    }

    public void solve() {
        LeastSquaresOptimizer.Optimum optimum = OPTIMIZER.optimize(this.problem);
        this.basePower = optimum.getPoint().getEntry(0);
        this.mediumCoeff = optimum.getPoint().getEntry(1);
    }

    public float getMediumCoeff() {
        return (float)this.mediumCoeff;
    }

    public float getBasePower() {
        return (float)this.basePower;
    }


    private LeastSquaresProblem createProblem(List<Double> measuredPowers, List<Double> realDistances) {
        return new LeastSquaresBuilder().
                start(new double[] {PWR_SEED, COEFF_SEED}).
                model(new OptimizedPowerTransformerJacobianFunction(measuredPowers)).
                target(toArray(realDistances)).
                lazyEvaluation(false).
                maxEvaluations(MAX_EVALUATIONS).
                maxIterations(MAX_ITERATIONS).
                build();
    }

    private static class OptimizedPowerTransformerJacobianFunction implements MultivariateJacobianFunction {

        private static final double LN10 = log(10);

        private final List<Double> measuredPowers;

        private OptimizedPowerTransformerJacobianFunction(List<Double> measuredPowers) {
            this.measuredPowers = measuredPowers;
        }

        @Override
        public Pair<RealVector, RealMatrix> value(RealVector testedValues) {
            //testedValues should be (basePower, C)

            double testedBasePower = testedValues.getEntry(0);
            double testedC = testedValues.getEntry(1);

            RealVector results = new ArrayRealVector(measuredPowers.size());
            RealMatrix jacobian = new Array2DRowRealMatrix(measuredPowers.size(), 2);

            for(int i = 0; i< measuredPowers.size() ; i++) {
                double measuredPower = measuredPowers.get(i);
                double computedDistance = computeDistance(measuredPower,testedBasePower,testedC);
                results.setEntry(i,computedDistance);
                jacobian.setEntry(i, 0, dfdBasePower(testedC, computedDistance));
                jacobian.setEntry(i, 1, dfdC(testedC, computedDistance));
            }

            return new Pair<>(results, jacobian);
        }

        private double computeDistance(double measuredPower,
                                       double basePower,
                                       double C) {
            double exponent = (basePower - measuredPower)/(10 * C);
            return pow(10, exponent);
        }

        /**
         * df(x)/dbasePower is [1n(10) * f(x)]/(10C)
         */
        private double dfdBasePower(double C,
                                    double fx) {
            return LN10 * fx * (1/(10*C));
        }

        /**
         * df(x)/dC is -[1n(10) * f(x) * log(f(x))]/C
         */
        private double dfdC(double C,
                            double fx) {
            return (-1) * LN10 * fx * log10(fx) * (1/C);
        }
    }
}
