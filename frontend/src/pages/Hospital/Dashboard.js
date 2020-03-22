import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@apollo/react-hooks';
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
import Button from '@material-ui/core/Button';

import { Typography } from '@material-ui/core';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

import Entry from './Entry';
import areasOfWork from '../../config/areas_of_work.json';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const SEARCH_QUERY = gql`
  query searchQuery($activities: [ID], $start: String!, $end: String!) {
    search(activities: $activities, start: $start, end: $end) {
      id
      qualification {
        name
      }
      activities {
        id
        name
      }
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
        activities {
          id
          name
        }
      }
      activity {
        id
        name
      }
      status
      startDate
      endDate
    }
  }
`;

const REQUEST_HELPER = gql`
  mutation requestHelper($helperId: ID) {
    requestHelper(helperId: $helperId) {
      id
      name
      email
      phone
      qualification {
        id
        name
      }
      activities {
        id
        name
      }
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
  cardsContainer: {
    width: 550,
  },
}));

export default function Dashboard() {
  const classes = useStyles();

  // Snackbar
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('Erfolg!');

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  };

  const [tabValue, setValue] = useState(0);
  const [filterValues, setFilterValues] = useState({});

  const [startDate, handleStartDateChange] = useState(new Date());
  const [endDate, handleEndDateChange] = useState(new Date());

  // Queries
  const { loading: searchLoading, data: searchData, refetch: searchRefetch } = useQuery(
    SEARCH_QUERY,
    {
      variables: {
        activities: Object.entries(filterValues)
          .filter(([, isFilterActive]) => isFilterActive)
          .map(([activityId]) => activityId),
        start: startDate.getTime().toString(),
        end: endDate.getTime().toString(),
      },
    },
  );

  const { loading: requestsLoading, data: requestsData, refetch: requestsRefetch } = useQuery(
    PERSONNEL_REQUESTS_QUERY,
    {
      variables: {
        // TODO query hospital of logged-in user before
        hospitalId: 'test',
        start: startDate.getTime().toString(),
        end: endDate.getTime().toString(),
      },
    },
  );

  // Mutation
  const [requestHelper] = useMutation(REQUEST_HELPER);

  // Sort requestsData into their categories
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

  // Re-fetch on filter change
  useEffect(() => {
    searchRefetch({
      activities: Object.entries(filterValues)
        .filter(([, isFilterActive]) => isFilterActive)
        .map(([activityId]) => activityId),
      start: startDate.getTime().toString(),
      end: endDate.getTime().toString(),
    });
  }, [filterValues, startDate, endDate, searchRefetch]);

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
            <Container className={classes.cardsContainer}>
              <Grid container className={classes.container} spacing={2} direction="column">
                {tabValue === 0
                  && searchData
                  && searchData.search.map((searchEntry) => (
                    <Grid item key={searchEntry.id}>
                      <Entry
                        id={searchEntry.id}
                        title={searchEntry.qualification.name}
                        skills={searchEntry.activities}
                      >
                        <Button
                          onClick={async () => {
                            try {
                              await requestHelper({
                                variables: {
                                  helperId: searchEntry.id,
                                },
                              });

                              setSnackbarMessage('Helfer erfolgreich angefragt!');
                              setSnackbarOpen(true);

                              searchRefetch({
                                activities: Object.entries(filterValues)
                                  .filter(([, isFilterActive]) => isFilterActive)
                                  .map(([activityId]) => activityId),
                                start: startDate.getTime().toString(),
                                end: endDate.getTime().toString(),
                              });

                              requestsRefetch({
                                // TODO query hospital of logged-in user before
                                hospitalId: 'test',
                                start: startDate.getTime().toString(),
                                end: endDate.getTime().toString(),
                              });
                            } catch (err) {
                              console.error(err);
                            }
                          }}
                          className={classes.button}
                          variant="contained"
                          size="small"
                        >
                          Anfragen
                        </Button>
                      </Entry>
                    </Grid>
                  ))}
                {tabValue === 1 && (
                  <>
                    <Typography color="secondary" gutterBottom>
                      ausstehend
                    </Typography>
                    {pendingRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pr.helper.qualification.name}
                          skills={pr.helper.activities}
                        ></Entry>
                      </Grid>
                    ))}
                    {pendingRequests.length === 0 && <Paper>Keine ausstehenden Anfragen.</Paper>}

                    <Divider variant="middle" />

                    <Typography color="textSecondary" gutterBottom>
                      abgelehnt
                    </Typography>
                    {declinedRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pr.helper.qualification.name}
                          skills={pr.helper.activities}
                        ></Entry>
                      </Grid>
                    ))}
                    {declinedRequests.length === 0 && <Paper>Keine abgelehnten Anfragen.</Paper>}
                  </>
                )}
                {tabValue === 2 && (
                  <>
                    <Typography color="secondary" gutterBottom>
                      aktiv
                    </Typography>
                    {activeRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pr.helper.qualification.name}
                          skills={pr.helper.activities}
                        ></Entry>
                      </Grid>
                    ))}
                    {activeRequests.length === 0 && <Paper>Keine aktiven Helfer.</Paper>}

                    <Typography color="textSecondary" gutterBottom>
                      abgelaufen
                    </Typography>
                    {expiredRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pr.helper.qualification.name}
                          skills={pr.helper.activities}
                        ></Entry>
                      </Grid>
                    ))}
                    {expiredRequests.length === 0 && <Paper>Keine abgelaufen Helfer.</Paper>}
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
                        control={
                          <Checkbox
                            checked={!!filterValues[area.id]}
                            name={area.id}
                            onChange={(e) => {
                              const targetName = e.target.name;
                              const targetChecked = e.target.checked;

                              setFilterValues((fv) => ({ ...fv, [targetName]: targetChecked }));
                            }}
                          />
                        }
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
      <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={handleSnackbarClose}>
        <Alert onClose={handleSnackbarClose} severity="success">
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </MuiPickersUtilsProvider>
  );
}
