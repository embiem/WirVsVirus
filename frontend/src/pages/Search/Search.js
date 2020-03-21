import React, { useState } from 'react';
import { useQuery } from '@apollo/react-hooks';
import { gql } from 'apollo-boost';

import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

import { MuiPickersUtilsProvider, KeyboardDatePicker } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';
import deLocale from 'date-fns/locale/de';

import { Typography } from '@material-ui/core';
import SearchEntry from './Entry';

const SEARCH_QUERY = gql`
  query searchQuery($activities: [Activity]) {
    search(activities: $activities) {
      id
      qualification {
        name
      }
      activities
    }
  }
`;

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  container: {
    margin: '12px 0',
  },
}));

export default function Search() {
  const { loading, data } = useQuery(SEARCH_QUERY, {
    variables: {
      activities: ['Hotline', 'Swap'],
    },
  });

  // TODO use navigation instead of tabs,
  // TODO as we want to navigate between pages for search/requests/my helpers
  const [tabValue, setValue] = useState(0);

  const [selectedDate, handleDateChange] = useState(new Date());

  const classes = useStyles();

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils} locale={deLocale}>
      <Container>
        <Paper square>
          <Tabs
            value={tabValue}
            onChange={handleChange}
            variant="fullWidth"
            indicatorColor="primary"
            textColor="primary"
            aria-label="icon tabs example"
          >
            <Tab label="Suche" />
            <Tab label="Anfragen" />
            <Tab label="Meine Helfer" />
          </Tabs>
        </Paper>

        <Grid container wrap="nowrap">
          <Grid item>
            <Container maxWidth="sm">
              {/* <Grid container className={classes.container} justify="flex-end">
                <FormControl className={classes.formControl}>
                  <InputLabel id="demo-simple-select-label">Priorisierung</InputLabel>
                  <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={'Zeitraum'}
                  >
                    <MenuItem value={'Zeitraum'}>Zeitraum</MenuItem>
                    <MenuItem value={'Skills'}>Skills</MenuItem>
                  </Select>
                </FormControl>
              </Grid> */}
              <Grid container className={classes.container} spacing={2} direction="column">
                {tabValue === 0
                  && data
                  && data.search.map((searchEntry) => (
                    <Grid item key={searchEntry.id}>
                      <SearchEntry
                        searchEntry={searchEntry}
                        onPrimaryButtonClick={() => {
                          // TODO
                          console.warn(`Not Yet Implemented: Helfer ${searchEntry.id} Anfragen`);
                        }}
                      />
                    </Grid>
                  ))}
                {tabValue === 0 && loading && <p>Loading ...</p>}
              </Grid>
            </Container>
          </Grid>
          <Grid item>
            <List>
              <ListItem className={classes.container}>
                <KeyboardDatePicker
                  value={selectedDate}
                  onChange={handleDateChange}
                  variant="inline"
                  inputVariant="outlined"
                  label="Von"
                  format="d. MMM yyyy"
                />
                <div style={{ width: 8 }} />
                <KeyboardDatePicker
                  value={selectedDate}
                  onChange={handleDateChange}
                  variant="inline"
                  inputVariant="outlined"
                  label="Bis"
                  format="d. MMM yyyy"
                />
              </ListItem>
              <Divider component="li" />
              <li>
                <Typography color="textSecondary" display="block" variant="caption">
                  Administration
                </Typography>
              </li>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Personalabteilung"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Kommunikation"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="IT-Unterstützung"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Buchhaltung"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Rechtsabteilung"
                />
              </ListItem>
              <Divider component="li" />
              <li>
                <Typography color="textSecondary" display="block" variant="caption">
                  Logistik
                </Typography>
              </li>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Planung, Materialbeschaffung"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="logistische Hilfsarbeiten, wie Krankentransport, Bluttransport, RTW"
                />
              </ListItem>
              <Divider component="li" />
              <li>
                <Typography color="textSecondary" display="block" variant="caption">
                  Medizin
                </Typography>
              </li>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Beratung (Hotline/Mail)"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Aufnahmebereich PatientInnen"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Normalstation – Pflege"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Intensivstation – Pflege"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Intensivstation – med. Versorgung ohne Beatmung"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Intensivstation – med. Versorgung mit Beatmung"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Beatmung verändern (Assistenz- / Facharzt)"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Operativer Tätigkeitsbereich"
                />
              </ListItem>
              <ListItem>
                <FormControlLabel
                  control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                  label="Weitere Tätigkeitsbereiche mit med. Vorausbildung"
                />
              </ListItem>
            </List>
          </Grid>
        </Grid>
      </Container>
    </MuiPickersUtilsProvider>
  );
}
