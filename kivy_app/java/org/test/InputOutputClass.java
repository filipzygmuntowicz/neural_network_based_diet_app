package org.test;
import java.util.Map;
import java.util.TreeMap;
import java.nio.ByteBuffer;
import java.util.List;

public class InputOutputClass {

    public Object get_input(ByteBuffer inputData){
        Object[] inputs = new Object[1];
        inputs[0] = inputData;
        return inputs;
    }

    public Map<Integer, Object> get_output(){
        Map<Integer, Object> outputMap = new TreeMap<>();
        float[][][] boxes = new float[1][10][4];
        float[][] scores = new float[1][10];
        float[] notImportant = new float[1];
        float[][] classes = new float[1][10];
        outputMap.put(0, scores);
        outputMap.put(1, boxes);
        outputMap.put(2, notImportant);
        outputMap.put(3, classes);
        return outputMap;
    }
}
