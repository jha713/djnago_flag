// App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [employees, setEmployees] = useState([]);
  const [flagStatus, setFlagStatus] = useState(false);
  const [newEmployee, setNewEmployee] = useState({ name: '', age: '', department: '' });
  const [updateEmployee, setUpdateEmployee] = useState({ id: null, name: '', age: '', department: '' });

  useEffect(() => {
    // Fetch flag status
    axios.get('http://localhost:8007/flag-status/')  // Adjust the URL as per your Django backend
      .then(response => {
        setFlagStatus(response.data.flag_status);
      })
      .catch(error => {
        console.error('Error fetching flag status:', error);
      });

    // Fetch employees if flag is enabled
    if (flagStatus) {
      axios.get('http://localhost:8007/employees/')  // Adjust the URL as per your Django backend
        .then(response => {
          setEmployees(response.data);
        })
        .catch(error => {
          console.error('Error fetching employees:', error);
        });
    }
  }, [flagStatus]);

  const handleCreateEmployee = () => {
    if (flagStatus) {
      axios.post('http://localhost:8007/employees/', newEmployee)
        .then(response => {
          setEmployees([...employees, response.data]);
          setNewEmployee({ name: '', age: '', department: '' });
        })
        .catch(error => {
          console.error('Error creating employee:', error);
        });
    } else {
      alert("You are not allowed to create new employees because the feature flag is off.");
    }
  };

  const handleUpdateEmployee = (employee) => {
    setUpdateEmployee(employee);
  };

  const handleUpdateFormSubmit = () => {
    axios.put(`http://localhost:8007/employees/${updateEmployee.id}/`, updateEmployee)
      .then(response => {
        const updatedEmployees = employees.map(emp => {
          if (emp.id === updateEmployee.id) {
            return response.data;
          }
          return emp;
        });
        setEmployees(updatedEmployees);
        setUpdateEmployee({ id: null, name: '', age: '', department: '' });
      })
      .catch(error => {
        console.error('Error updating employee:', error);
      });
  };

  const handleDeleteEmployee = (id) => {
    if (flagStatus) {
      axios.delete(`http://localhost:8007/employees/${id}/`)
        .then(() => {
          const updatedEmployees = employees.filter(emp => emp.id !== id);
          setEmployees(updatedEmployees);
        })
        .catch(error => {
          console.error('Error deleting employee:', error);
        });
    } else {
      alert("You are not allowed to delete employees because the feature flag is off.");
    }
  };

  return (
    <div className="App">
      <h1>Employees</h1>
      <div className="form">
        <h2>Create Employee</h2>
        <input
          type="text"
          placeholder="Name"
          value={newEmployee.name}
          onChange={e => setNewEmployee({ ...newEmployee, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Age"
          value={newEmployee.age}
          onChange={e => setNewEmployee({ ...newEmployee, age: e.target.value })}
        />
        <input
          type="text"
          placeholder="Department"
          value={newEmployee.department}
          onChange={e => setNewEmployee({ ...newEmployee, department: e.target.value })}
        />
        <button onClick={handleCreateEmployee} disabled={!flagStatus} className="btn btn-primary">Create</button>
      </div>
      <ul>
        {employees.map(employee => (
          <li key={employee.id}>
            {employee.name}
            <button onClick={() => handleUpdateEmployee(employee)} className="btn btn-warning">Update</button>
            <button onClick={() => handleDeleteEmployee(employee.id)} disabled={!flagStatus} className="btn btn-danger">Delete</button>
          </li>
        ))}
      </ul>
      {updateEmployee.id && (
        <div className="form">
          <h2>Update Employee</h2>
          <input
            type="text"
            placeholder="Name"
            value={updateEmployee.name}
            onChange={e => setUpdateEmployee({ ...updateEmployee, name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Age"
            value={updateEmployee.age}
            onChange={e => setUpdateEmployee({ ...updateEmployee, age: e.target.value })}
          />
          <input
            type="text"
            placeholder="Department"
            value={updateEmployee.department}
            onChange={e => setUpdateEmployee({ ...updateEmployee, department: e.target.value })}
          />
          <button onClick={handleUpdateFormSubmit} className="btn btn-primary">Update</button>
          <button onClick={() => setUpdateEmployee({ id: null, name: '', age: '', department: '' })} className="btn btn-secondary">Cancel</button>
        </div>
      )}
    </div>
  );
}

export default App;
