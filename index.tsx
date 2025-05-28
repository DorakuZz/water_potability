import React, { useState } from 'react';
import { 
  ScrollView, 
  Text, 
  View, 
  TouchableOpacity, 
  StyleSheet, 
  Alert, 
  ActivityIndicator,
  Dimensions 
} from 'react-native';

const { width } = Dimensions.get('window');

interface DataType {
  ph: number;
  hardness: number;
  solids: number;
  chloramines: number;
  sulfate: number;
  conductivity: number;
  organic_carbon: number;
  trihalomethanes: number;
  turbidity: number;
}

const initialData: DataType = {
  ph: 7,
  hardness: 150,
  solids: 10000,
  chloramines: 7,
  sulfate: 250,
  conductivity: 500,
  organic_carbon: 15,
  trihalomethanes: 60,
  turbidity: 5,
};

const sliderRanges: Record<keyof DataType, [number, number]> = {
  ph: [0, 14],
  hardness: [50, 300],
  solids: [2000, 50000],
  chloramines: [0, 15],
  sulfate: [50, 500],
  conductivity: [100, 1000],
  organic_carbon: [0, 30],
  trihalomethanes: [0, 120],
  turbidity: [0, 10],
};

const parameterNames: Record<keyof DataType, string> = {
  ph: 'pH',
  hardness: 'Dureza',
  solids: 'Sólidos Totales',
  chloramines: 'Cloraminas',
  sulfate: 'Sulfatos',
  conductivity: 'Conductividad',
  organic_carbon: 'Carbono Orgánico',
  trihalomethanes: 'Trihalometanos',
  turbidity: 'Turbidez',
};

interface CustomSliderProps {
  value: number;
  min: number;
  max: number;
  onValueChange: (value: number) => void;
  step?: number;
}

const CustomSlider: React.FC<CustomSliderProps> = ({ 
  value, 
  min, 
  max, 
  onValueChange, 
  step = 0.1 
}) => {
  const [isPressed, setIsPressed] = useState(false);
  
  const handlePress = (event: any) => {
    const { locationX } = event.nativeEvent;
    const sliderWidth = width - 64;
    const percentage = locationX / sliderWidth;
    const newValue = min + (percentage * (max - min));
    const steppedValue = Math.round(newValue / step) * step;
    const clampedValue = Math.max(min, Math.min(max, steppedValue));
    onValueChange(clampedValue);
  };

  const thumbPosition = ((value - min) / (max - min)) * (width - 64);

  return (
    <View style={styles.sliderContainer}>
      <TouchableOpacity
        style={styles.sliderTrack}
        onPress={handlePress}
        onPressIn={() => setIsPressed(true)}
        onPressOut={() => setIsPressed(false)}
        activeOpacity={1}
      >
        <View style={[styles.sliderFill, { width: thumbPosition }]} />
        <View 
          style={[
            styles.sliderThumb, 
            { left: thumbPosition - 12 },
            isPressed && styles.sliderThumbPressed
          ]} 
        />
      </TouchableOpacity>
    </View>
  );
};

export default function App() {
  const [data, setData] = useState<DataType>(initialData);
  const [result, setResult] = useState<number | string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleChange = (key: keyof DataType, value: number) => {
    setData({ ...data, [key]: value });
  };

  const predict = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      const response = await fetch('https://water-potability-1-vdzg.onrender.com/predict', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const json = await response.json();
      
      if (json.potability !== undefined) {
        setResult(json.potability);
      } else {
        throw new Error('Respuesta inválida del servidor');
      }
    } catch (error) {
      console.error('Error en la predicción:', error);
      setResult('Error');
      
      Alert.alert(
        'Error de Conexión',
        'No se pudo conectar con el servidor. Verifica tu internet e intenta nuevamente.',
        [{ text: 'OK' }]
      );
    } finally {
      setLoading(false);
    }
  };

  const getResultColor = (): string => {
    if (result === 1) return '#4CAF50';
    if (result === 0) return '#FF5722';
    return '#FF9800';
  };

  const getResultText = (): string => {
    if (result === 1) return '✅ Agua Potable';
    if (result === 0) return '❌ Agua No Potable';
    return '⚠️ Error en la predicción';
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>🔬 Predicción de Potabilidad</Text>
      
      <Text style={styles.subtitle}>
        Ajusta los parámetros para analizar el agua
      </Text>

      {(Object.entries(data) as Array<[keyof DataType, number]>).map(([key, value]) => (
        <View key={key} style={styles.parameterContainer}>
          <View style={styles.labelContainer}>
            <Text style={styles.label}>
              {parameterNames[key]}
            </Text>
            <Text style={styles.valueText}>{value.toFixed(2)}</Text>
          </View>
          
          <CustomSlider
            value={value}
            min={sliderRanges[key][0]}
            max={sliderRanges[key][1]}
            onValueChange={(val) => handleChange(key, val)}
          />
          
          <View style={styles.rangeContainer}>
            <Text style={styles.rangeText}>{sliderRanges[key][0]}</Text>
            <Text style={styles.rangeText}>{sliderRanges[key][1]}</Text>
          </View>
        </View>
      ))}

      <View style={styles.buttonContainer}>
        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#2196F3" />
            <Text style={styles.loadingText}>Analizando agua...</Text>
          </View>
        ) : (
          <TouchableOpacity style={styles.button} onPress={predict}>
            <Text style={styles.buttonText}>🔍 Analizar Potabilidad</Text>
          </TouchableOpacity>
        )}
      </View>

      {result !== null && !loading && (
        <View style={[styles.resultContainer, { borderColor: getResultColor() }]}>
          <Text style={[styles.result, { color: getResultColor() }]}>
            {getResultText()}
          </Text>
          {result !== 'Error' && (
            <Text style={styles.resultDescription}>
              {result === 1 
                ? 'El agua cumple con los estándares de potabilidad' 
                : 'El agua no cumple con los estándares de potabilidad'
              }
            </Text>
          )}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: '#121212',
    minHeight: '100%',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
    color: '#FFFFFF',
  },
  subtitle: {
    fontSize: 14,
    textAlign: 'center',
    color: '#B0B0B0',
    marginBottom: 20,
  },
  parameterContainer: {
    marginBottom: 20,
    backgroundColor: '#1E1E1E',
    padding: 16,
    borderRadius: 12,
  },
  labelContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  label: {
    fontWeight: '600',
    color: '#FFFFFF',
    fontSize: 16,
  },
  valueText: {
    color: '#2196F3',
    fontWeight: 'bold',
    fontSize: 16,
  },
  sliderContainer: {
    marginVertical: 8,
  },
  sliderTrack: {
    height: 6,
    backgroundColor: '#333333',
    borderRadius: 3,
    position: 'relative',
  },
  sliderFill: {
    height: 6,
    backgroundColor: '#2196F3',
    borderRadius: 3,
  },
  sliderThumb: {
    position: 'absolute',
    top: -9,
    width: 24,
    height: 24,
    backgroundColor: '#2196F3',
    borderRadius: 12,
    borderWidth: 3,
    borderColor: '#FFFFFF',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,
  },
  sliderThumbPressed: {
    transform: [{ scale: 1.2 }],
  },
  rangeContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  rangeText: {
    fontSize: 12,
    color: '#888888',
  },
  buttonContainer: {
    marginTop: 20,
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#2196F3',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    color: '#FFFFFF',
    marginTop: 10,
    fontSize: 16,
  },
  resultContainer: {
    backgroundColor: '#1E1E1E',
    padding: 20,
    borderRadius: 12,
    borderWidth: 2,
    alignItems: 'center',
  },
  result: {
    fontSize: 20,
    textAlign: 'center',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  resultDescription: {
    fontSize: 14,
    textAlign: 'center',
    color: '#B0B0B0',
  },
});