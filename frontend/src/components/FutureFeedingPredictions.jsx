import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const FutureFeedingPredictions = () => {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5001/predict/next-feeding")
      .then((res) => {
        setPredictions(res.data || []);
      })
      .catch((err) => console.error("Error fetching predictions:", err));
  }, []);

  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle>Future Feeding Predictions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Predicted Time</TableHead>
                <TableHead className="text-right">Confidence (%)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {predictions.map((feeding, index) => (
                <TableRow key={index}>
                  <TableCell>{feeding.predicted_time}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-2">
                      <div className="w-24 h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full ${
                            feeding.confidence > 90 ? 'bg-tummy-green' : 
                            feeding.confidence > 80 ? 'bg-tummy-yellow' : 'bg-tummy-red'
                          }`}
                          style={{ width: `${feeding.confidence}%` }}
                        ></div>
                      </div>
                      <span>{feeding.confidence}%</span>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};

export default FutureFeedingPredictions;
