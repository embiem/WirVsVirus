import React, { useState, useEffect } from 'react';
import { useQuery } from '@apollo/react-hooks';
import { gql } from 'apollo-boost';

import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';

import { MuiPickersUtilsProvider, KeyboardDatePicker } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import deLocale from 'date-fns/locale/de';

import { Typography } from '@material-ui/core';

import SearchEntry from './Entry';
import areasOfWork from '../../config/areas_of_work.json';

const SEARCH_QUERY = gql`
  query searchQuery($activities: [Activity], $start: String!, $end: String!) {
    search(activities: $activities, start: $start, end: $end) {
      id
      qualification {
        name
      }
      activities
    }
  }
`;

const PERSONNEL_REQUESTS_QUERY = gql`
  query personnelRequestsQuery($hospitalId: ID, $start: String!, $end: String!) {
    personnelRequests(hospitalId: $hospitalId, start: $start, end: $end) {
      id
      helper {
        qualification {
          name
        }
        activities
      }
      activity
      status
      startDate
      endDate
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

export default function Dashboard() {
  const [tabValue, setValue] = useState(0);

  const [startDate, handleStartDateChange] = useState(new Date());
  const [endDate, handleEndDateChange] = useState(new Date());

  const { loading: searchLoading, data: searchData } = useQuery(SEARCH_QUERY, {
    variables: {
      // TODO get from filters
      activities: ['Hotline', 'Swap'],
      start: startDate.getTime().toString(),
      end: endDate.getTime().toString(),
    },
  });

  const { loading: requestsLoading, data: requestsData } = useQuery(PERSONNEL_REQUESTS_QUERY, {
    variables: {
      // TODO query hospital of logged-in user before
      hospitalId: 'test',
      start: startDate.getTime().toString(),
      end: endDate.getTime().toString(),
    },
  });

  const classes = useStyles();

  const [pendingRequests, setPendingRequests] = useState([]);
  const [declinedRequests, setDeclinedRequests] = useState([]);
  const [activeRequests, setActiveRequests] = useState([]);
  const [expiredRequests, setExpiredRequests] = useState([]);

  useEffect(() => {
    const pending = [];
    const declined = [];
    const active = [];
    const expired = [];

    if (requestsData && requestsData.personnelRequests) {
      requestsData.personnelRequests.forEach((pr) => {
        if (pr.status === 'Pending') {
          pending.push(pr);
        } else if (pr.status === 'Declined') {
          declined.push(pr);
        } else if (pr.status === 'Accepted') {
          // TODO needs to correctly check days
          const curDate = new Date().getTime();
          if (pr.startDate < curDate && pr.endDate > curDate) {
            active.push(pr);
          } else {
            expired.push(pr);
          }
        }
      });
    }
    setPendingRequests(pending);
    setDeclinedRequests(declined);
    setActiveRequests(active);
    setExpiredRequests(expired);
  }, [requestsData]);

  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils} locale={deLocale}>
      <Container>
        <Paper square>
          <Tabs
            value={tabValue}
            onChange={(event, newValue) => {
              setValue(newValue);
            }}
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
              <Grid container className={classes.container} spacing={2} direction="column">
                {tabValue === 0
                  && searchData
                  && searchData.search.map((searchEntry) => (
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
                {tabValue === 1 && (
                  <>
                    <p>ausstehend</p>
                    {pendingRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <pre>{JSON.stringify(pr, null, 2)}</pre>
                      </Grid>
                    ))}
                    <p>abgelehnt</p>
                    {declinedRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <pre>{JSON.stringify(pr, null, 2)}</pre>
                      </Grid>
                    ))}
                  </>
                )}
                {tabValue === 2 && (
                  <>
                    <p>aktiv</p>
                    {activeRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <pre>{JSON.stringify(pr, null, 2)}</pre>
                      </Grid>
                    ))}
                    <p>abgelaufen</p>
                    {expiredRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <pre>{JSON.stringify(pr, null, 2)}</pre>
                      </Grid>
                    ))}
                  </>
                )}
                {tabValue === 0 && searchLoading && <p>Lade Helfer ...</p>}
                {tabValue === 1 && requestsLoading && <p>Lade Anfragen ...</p>}
                {tabValue === 2 && requestsLoading && <p>Lade Helfer ...</p>}
              </Grid>
            </Container>
          </Grid>
          <Grid item>
            <List>
              <ListItem className={classes.container}>
                <KeyboardDatePicker
                  value={startDate}
                  onChange={handleStartDateChange}
                  variant="inline"
                  inputVariant="outlined"
                  label="Von"
                  format="d. MMM yyyy"
                />
                <div style={{ width: 8 }} />
                <KeyboardDatePicker
                  value={endDate}
                  onChange={handleEndDateChange}
                  variant="inline"
                  inputVariant="outlined"
                  label="Bis"
                  format="d. MMM yyyy"
                />
              </ListItem>

              {areasOfWork.categories.map((category) => (
                <React.Fragment key={category.id}>
                  <Divider component="li" />
                  <li>
                    <Typography color="textSecondary" display="block" variant="caption">
                      {category.name.de}
                    </Typography>
                  </li>
                  {category.children.map((area) => (
                    <ListItem key={area.id}>
                      <FormControlLabel
                        control={<Checkbox checked={true} onChange={() => {}} name="checkedA" />}
                        label={area.name.de}
                      />
                    </ListItem>
                  ))}
                </React.Fragment>
              ))}
            </List>
          </Grid>
        </Grid>
      </Container>
    </MuiPickersUtilsProvider>
  );
}
