import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Chip from '@material-ui/core/Chip';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const useStyles = makeStyles({
  root: {
    minWidth: 450,
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  button: {
    marginLeft: 'auto',
  },
  table: {
    border: 'none',
    padding: 8,
  },
  cardActions: {
    padding: 16,
  },
});

export default function OutlinedCard(props) {
  const { id, qualification, activities } = props.searchEntry;
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardContent>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell className={classes.table}>{qualification.name}</TableCell>
                <TableCell className={classes.table} align="right">
                  ID ${id}
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell className={classes.table}>Hoechster Abschluss:</TableCell>
                <TableCell className={classes.table} align="right">
                  1. Staatsexamen
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className={classes.table}>Verfuegbarer Zeitraum:</TableCell>
                <TableCell className={classes.table} align="right">
                  1.1.1 bis 2.2.2.
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className={classes.table}>Skills:</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className={classes.table}>
                  <Grid container spacing={2}>
                    {activities.map((ac) => (
                      <Grid item key={ac}>
                        <Chip key={ac} label={ac} />
                      </Grid>
                    ))}
                  </Grid>
                </TableCell>
                <TableCell className={classes.table} align="right">
                  <Button onClick={props.onPrimaryButtonClick} className={classes.button} variant="contained" size="small">
                    Anfragen
                  </Button>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
}
