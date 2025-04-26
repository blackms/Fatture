import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon,
  Comment as CommentIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const InvoiceDialog = ({ open, onClose, onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    invoice_type: 'expense',
    amount: '',
    date: new Date(),
    description: '',
    supplier_name: '',
    customer_name: '',
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        ...initialData,
        date: new Date(initialData.date),
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {initialData ? 'Edit Invoice' : 'Add New Invoice'}
      </DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          <FormControl fullWidth margin="normal">
            <InputLabel>Type</InputLabel>
            <Select
              name="invoice_type"
              value={formData.invoice_type}
              label="Type"
              onChange={handleChange}
            >
              <MenuItem value="expense">Expense</MenuItem>
              <MenuItem value="revenue">Revenue</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="normal"
            required
            fullWidth
            name="amount"
            label="Amount"
            type="number"
            value={formData.amount}
            onChange={handleChange}
          />
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DatePicker
              label="Date"
              value={formData.date}
              onChange={(date) =>
                setFormData((prev) => ({ ...prev, date }))
              }
              renderInput={(params) => (
                <TextField {...params} fullWidth margin="normal" />
              )}
            />
          </LocalizationProvider>
          <TextField
            margin="normal"
            fullWidth
            name="description"
            label="Description"
            multiline
            rows={2}
            value={formData.description}
            onChange={handleChange}
          />
          {formData.invoice_type === 'expense' ? (
            <TextField
              margin="normal"
              required
              fullWidth
              name="supplier_name"
              label="Supplier Name"
              value={formData.supplier_name}
              onChange={handleChange}
            />
          ) : (
            <TextField
              margin="normal"
              required
              fullWidth
              name="customer_name"
              label="Customer Name"
              value={formData.customer_name}
              onChange={handleChange}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained">
            {initialData ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

const Invoices = () => {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    try {
      const response = await axios.get('/api/invoices/');
      setInvoices(response.data.results);
    } catch (error) {
      setError('Failed to load invoices');
    } finally {
      setLoading(false);
    }
  };

  const handleAddInvoice = () => {
    setSelectedInvoice(null);
    setDialogOpen(true);
  };

  const handleEditInvoice = (invoice) => {
    setSelectedInvoice(invoice);
    setDialogOpen(true);
  };

  const handleDeleteInvoice = async (id) => {
    if (window.confirm('Are you sure you want to delete this invoice?')) {
      try {
        await axios.delete(`/api/invoices/${id}/`);
        fetchInvoices();
      } catch (error) {
        setError('Failed to delete invoice');
      }
    }
  };

  const handleSubmitInvoice = async (formData) => {
    try {
      if (selectedInvoice) {
        await axios.put(`/api/invoices/${selectedInvoice.id}/`, formData);
      } else {
        await axios.post('/api/invoices/', formData);
      }
      setDialogOpen(false);
      fetchInvoices();
    } catch (error) {
      setError('Failed to save invoice');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'uploaded':
        return 'default';
      case 'reviewed':
        return 'primary';
      case 'processed':
        return 'success';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Invoices</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddInvoice}
        >
          Add Invoice
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {invoices.map((invoice) => (
              <TableRow key={invoice.id}>
                <TableCell>{new Date(invoice.date).toLocaleDateString()}</TableCell>
                <TableCell>{invoice.invoice_type}</TableCell>
                <TableCell>${invoice.amount}</TableCell>
                <TableCell>{invoice.description}</TableCell>
                <TableCell>
                  <Chip
                    label={invoice.status}
                    color={getStatusColor(invoice.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => window.open(invoice.file_url, '_blank')}
                  >
                    <VisibilityIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleEditInvoice(invoice)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDeleteInvoice(invoice.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <InvoiceDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSubmit={handleSubmitInvoice}
        initialData={selectedInvoice}
      />
    </Box>
  );
};

export default Invoices; 