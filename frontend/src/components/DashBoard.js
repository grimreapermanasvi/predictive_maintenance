import React, { useState, useEffect } from 'react';
import SensorChart from './SensorChart';
import AlertPanel from './AlertPanel';

const Dashboard = () => {
    const [currentData, setCurrentData] = useState(null);
    const [historicalData, setHistoricalData] = useState([]);

    useEffect(() => {
        // Fetch historical data initially
        fetchHistoricalData();

        // Set up polling for current data
        const interval = setInterval(fetchCurrentData, 1000);
        return () => clearInterval(interval);
    }, []);

    const fetchCurrentData = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/current-data');
            const data = await response.json();
            setCurrentData(data);
            
            // Update historical data
            setHistoricalData(prev => {
                const updated = [...prev, data.sensor_data];
                return updated.slice(-100); // Keep last 100 points
            });
        } catch (error) {
            console.error('Error fetching current data:', error);
        }
    };

    const fetchHistoricalData = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/historical-data');
            const data = await response.json();
            setHistoricalData(data);
        } catch (error) {
            console.error('Error fetching historical data:', error);
        }
    };

    const handleReset = async () => {
        try {
            await fetch('http://localhost:5000/api/reset', {
                method: 'POST'
            });
            fetchHistoricalData();
        } catch (error) {
            console.error('Error resetting simulation:', error);
        }
    };

    if (!currentData) {
        return <div>Loading...</div>;
    }

    return (
        <div className="p-4">
            <div className="mb-4">
                <h1 className="text-2xl font-bold mb-2">Equipment Monitoring Dashboard</h1>
                <button 
                    onClick={handleReset}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                    Reset Simulation
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg shadow">
                    <h2 className="text-xl font-semibold mb-4">Current Readings</h2>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-gray-600">Temperature</p>
                            <p className="text-2xl">{currentData.sensor_data.temperature}°C</p>
                        </div>
                        <div>
                            <p className="text-gray-600">Vibration</p>
                            <p className="text-2xl">{currentData.sensor_data.vibration} Hz</p>
                        </div>
                    </div>
                </div>

                <AlertPanel 
                    prediction={currentData.prediction}
                    state={currentData.sensor_data.state}
                />
            </div>

            <div className="mt-4">
                <SensorChart data={historicalData} />
            </div>
        </div>
    );
};

export default Dashboard;