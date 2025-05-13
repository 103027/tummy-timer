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

const FeedingHistoryTable = () => {
  const [feedingHistory, setFeedingHistory] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5001/history")
      .then((res) => {
        const formatted = res.data.map((entry, index) => {
          const ts = new Date(entry.timestamp);
          return {
            id: index,
            date: ts.toLocaleDateString(),
            time: ts.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            amount: entry.weight
          };
        });
        setFeedingHistory(formatted);
      })
      .catch((err) => console.error("Error fetching feeding history:", err));
  }, []);

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle>Feeding History</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64 overflow-y-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Time</TableHead>
                <TableHead className="text-right">Amount (g)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {feedingHistory.map((feeding) => (
                <TableRow key={feeding.id}>
                  <TableCell>{feeding.date}</TableCell>
                  <TableCell>{feeding.time}</TableCell>
                  <TableCell className="text-right">{feeding.amount}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};

export default FeedingHistoryTable;
