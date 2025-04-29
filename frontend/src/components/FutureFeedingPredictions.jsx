import React from 'react';
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Sample data for demonstration
const futureFeedingData = [
  { id: 1, time: "06:00 PM", confidence: 95 },
  { id: 2, time: "08:00 AM (Tomorrow)", confidence: 92 },
  { id: 3, time: "12:30 PM (Tomorrow)", confidence: 88 },
];

const FutureFeedingPredictions = () => {
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
              {futureFeedingData.map((feeding) => (
                <TableRow key={feeding.id}>
                  <TableCell>{feeding.time}</TableCell>
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
