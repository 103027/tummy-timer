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
const feedingHistoryData = [
  { id: 1, date: "2025-04-28", time: "08:00 AM", amount: 25 },
  { id: 2, date: "2025-04-28", time: "12:30 PM", amount: 30 },
  { id: 3, date: "2025-04-27", time: "08:15 AM", amount: 25 },
  { id: 4, date: "2025-04-27", time: "12:45 PM", amount: 30 },
  { id: 5, date: "2025-04-27", time: "06:00 PM", amount: 25 },
];

const FeedingHistoryTable = () => {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle>Feeding History</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Time</TableHead>
                <TableHead className="text-right">Amount (g)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {feedingHistoryData.map((feeding) => (
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
