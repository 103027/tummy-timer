import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Clock, CalendarClock, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import axios from "axios";
import { useState, useEffect } from "react";

const FeedingSchedule = () => {
  const [schedules, setSchedules] = useState([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newSchedule, setNewSchedule] = useState({
    startTime: "08:00",
    endTime: "09:00",
    portions: 1,
    days: []
  });
  const [statusMessage, setStatusMessage] = useState("");
  const [showStatus, setShowStatus] = useState(false);
  const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  const fetchSchedules = () => {
    axios.get("http://127.0.0.1:5001/schedule")
      .then((res) => {
        const data = res.data;
        if (data.startTime) setSchedules([data]); // if backend returns one object
        else if (Array.isArray(data)) setSchedules(data); // if returns array
      })
      .catch((err) => console.error("Failed to fetch schedules:", err));
  };

  useEffect(() => {
    fetchSchedules();
  }, []);

  const showTemporaryMessage = (message) => {
    setStatusMessage(message);
    setShowStatus(true);
    setTimeout(() => setShowStatus(false), 3000);
  };

  const handleSubmitSchedule = () => {
    if (newSchedule.startTime >= newSchedule.endTime) {
      showTemporaryMessage("Invalid time window: End time must be after start time.");
      return;
    }

    const payload = {
        startTime: newSchedule.startTime,
        endTime: newSchedule.endTime,
        portion: newSchedule.portions,
        days: newSchedule.days && newSchedule.days.length ? newSchedule.days : daysOfWeek
      };

    console.log("payload",payload);

    axios.post("http://127.0.0.1:5001/schedule", payload)
      .then(() => {
        fetchSchedules();
        setIsDialogOpen(false);
        showTemporaryMessage(`Feeding schedule added for ${payload.startTime} - ${payload.endTime} with ${payload.portions} portions of food.`);
        setNewSchedule({
            startTime: "08:00",
            endTime: "09:00",
            portions: 1,
            days: []
          });
      })
      .catch(err => {
        console.error("Error saving schedule:", err);
        showTemporaryMessage("Failed to save schedule.");
      });
  };

  const toggleDay = (day) => {
    setNewSchedule((prev) => ({
      ...prev,
      days: prev.days.includes(day)
        ? prev.days.filter(d => d !== day)
        : [...prev.days, day]
    }));
  };

  const deleteSchedule = async (index) => {
    try {
      const response = await fetch('http://127.0.0.1:5001/schedule/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ index }),
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to delete schedule');
      }
  
      const data = await response.json();
      setSchedules(data.remainingSchedules || []);
  
      showTemporaryMessage('Feeding schedule has been removed.');
    } catch (error) {
      console.error('Error deleting schedule:', error);
      showTemporaryMessage(`Error: ${error.message}`, 'error');
    }
  };
  

  return (
    <Card className="h-full">
      <CardHeader className="pb-2 flex flex-row items-center justify-between">
        <CardTitle>Feeding Schedule</CardTitle>
        <Button variant="ghost" size="sm" onClick={() => setIsDialogOpen(true)}>
          <Plus size={16} className="mr-1" />
          Add Schedule
        </Button>
      </CardHeader>
      <CardContent>
        {showStatus && (
          <div className="bg-tummy-blue-light p-3 rounded-md text-sm animate-fade-in">
            {statusMessage}
          </div>
        )}
        {schedules.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <CalendarClock className="mx-auto h-12 w-12 opacity-50 mb-2" />
            <p>No feeding schedules yet</p>
          </div>
        ) : (
          schedules.map((schedule, idx) => (
            <div key={idx} className="flex items-center justify-between p-3 mt-2 border rounded-lg border-primary bg-primary/5">
              <div className="flex items-center">
                <div className="p-2 rounded-md bg-primary/10 mr-3">
                  <Clock size={18} className="text-primary" />
                </div>
                <div>
                  <p className="font-medium">{schedule.startTime} - {schedule.endTime}</p>
                  <div className="flex gap-1 mt-1">
                    {daysOfWeek.map((day) => (
                      <span key={day} className={`text-xs px-1 rounded ${schedule.days?.includes(day) ? 'bg-primary/20 text-primary-foreground' : 'bg-gray-100 text-gray-400'}`}>
                        {day[0]}
                      </span>
                    ))}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Portions: {schedule.portion}</p>
                </div>
              </div>
              <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-destructive hover:bg-destructive/10"
                    onClick={() => deleteSchedule(idx)}
                  >
                    Delete
                  </Button>
                </div>
            </div>
          ))
        )}

        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Feeding Schedule</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Start Time</label>
                  <Input type="time" value={newSchedule.startTime} onChange={(e) => setNewSchedule({ ...newSchedule, startTime: e.target.value })} />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">End Time</label>
                  <Input type="time" value={newSchedule.endTime} onChange={(e) => setNewSchedule({ ...newSchedule, endTime: e.target.value })} />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Portions (1 portion = 25g/1oz)</label>
                <Input type="number" value={newSchedule.portions} onChange={(e) => setNewSchedule({ ...newSchedule, portions: parseInt(e.target.value) || 0 })} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Days</label>
                <div className="flex flex-wrap gap-2">
                  {daysOfWeek.map((day) => (
                    <button key={day} type="button" onClick={() => toggleDay(day)}
                      className={`px-3 py-1 text-sm rounded-md ${newSchedule.days.includes(day) ? 'bg-primary text-primary-foreground' : 'bg-gray-100 hover:bg-gray-200'}`}>
                      {day}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
              <Button onClick={handleSubmitSchedule}>Save</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  );
};

export default FeedingSchedule;
