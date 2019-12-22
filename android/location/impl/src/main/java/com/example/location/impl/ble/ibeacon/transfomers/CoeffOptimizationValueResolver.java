package com.example.location.impl.ble.ibeacon.transfomers;

import com.example.location.api.entity.emitter.SignalEmitter;

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

import static com.example.location.impl.RadioDataTransformer.ONE_METER_POWER_SIGNAL_KEY;
import static com.google.common.primitives.Doubles.toArray;
import static java.lang.StrictMath.log;
import static java.lang.StrictMath.log10;
import static java.lang.StrictMath.pow;

/**
 * Run an optimization problem considering only the coefficient as variable
 */
public class CoeffOptimizationValueResolver implements OptimizationBasedValueResolver{

    private static final double COEFF_SEED = 1.0;
    private static final int MAX_ITERATIONS = 1000;
    private static final int MAX_EVALUATIONS = 1000;
    private static final LeastSquaresOptimizer OPTIMIZER = new LevenbergMarquardtOptimizer();

    private double coeff;
    private double calibratedBasePower;

    private LeastSquaresProblem problem;

    public static OptimizationBasedValueResolverFactory coeffOptimizationValueResolver() {
        return CoeffOptimizationValueResolver::new;
    }

    private CoeffOptimizationValueResolver(List<Double> realDistances, List<Double> measuredPowers, SignalEmitter signalEmitter) {
        this.calibratedBasePower = signalEmitter.getSignal().getAttribute(ONE_METER_POWER_SIGNAL_KEY).map(Double::parseDouble).orElse(-60.0);
        this.problem = createProblem(measuredPowers, realDistances, this.calibratedBasePower);
    }

    public void solve() {
        LeastSquaresOptimizer.Optimum optimum = OPTIMIZER.optimize(this.problem);
        this.coeff = optimum.getPoint().getEntry(0);
    }

    public float getMediumCoeff() {
        return (float)this.coeff;
    }

    public float getBasePower() {
        return (float)this.calibratedBasePower;
    }


    private LeastSquaresProblem createProblem(List<Double> measuredPowers,
                                              List<Double> realDistances,
                                              double calibratedBasePower) {
        return new LeastSquaresBuilder().
                start(new double[] {COEFF_SEED}).
                model(new CoeffOptimizationValueResolver.OptimizedPowerTransformerJacobianFunction(measuredPowers, calibratedBasePower)).
                target(toArray(realDistances)).
                lazyEvaluation(false).
                maxEvaluations(MAX_EVALUATIONS).
                maxIterations(MAX_ITERATIONS).
                build();
    }

    private static class OptimizedPowerTransformerJacobianFunction implements MultivariateJacobianFunction {

        private static final double LN10 = log(10);

        private final List<Double> measuredPowers;
        private final double calibratedBasePower;

        private OptimizedPowerTransformerJacobianFunction(List<Double> measuredPowers, double calibratedBasePower) {
            this.measuredPowers = measuredPowers;
            this.calibratedBasePower = calibratedBasePower;
        }

        @Override
        public Pair<RealVector, RealMatrix> value(RealVector testedValues) {
            //testedValues should be (C)

            double testedCoeff = testedValues.getEntry(0);

            RealVector results = new ArrayRealVector(measuredPowers.size());
            RealMatrix jacobian = new Array2DRowRealMatrix(measuredPowers.size(), 1);

            for(int i = 0; i< measuredPowers.size() ; i++) {
                double measuredPower = measuredPowers.get(i);
                double computedDistance = computeDistance(measuredPower,testedCoeff);
                results.setEntry(i,computedDistance);
                jacobian.setEntry(i, 0, dfdC(testedCoeff,computedDistance));
            }

            return new Pair<>(results, jacobian);
        }

        private double computeDistance(double measuredPower,
                                       double testedCoeff){
            double exponent = (calibratedBasePower - measuredPower)/(10 * testedCoeff);
            return pow(10, exponent);
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
