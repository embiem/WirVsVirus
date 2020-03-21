import React from 'react';
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
  priorityContainer: {
    margin: '12px 0',
  },
}));

export default function Search() {
  const { loading, data } = useQuery(SEARCH_QUERY, {
    variables: {
      activities: ['Hotline', 'Swap'],
    },
  });

  const [tabValue, setValue] = React.useState(0);

  const classes = useStyles();

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div>
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

      <Grid container>
        <Grid item>
          <Container maxWidth="sm">
            <Grid container className={classes.priorityContainer} justify="flex-end">
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
            </Grid>
            <Grid container spacing={2} direction="column">
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
          <Container>Filter</Container>
        </Grid>
      </Grid>
    </div>
  );
}
