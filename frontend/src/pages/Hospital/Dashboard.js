import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@apollo/react-hooks';
import { gql } from 'apollo-boost';
import { Link } from '@reach/router';

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
import Radio from '@material-ui/core/Radio';
import deLocale from 'date-fns/locale/de';
import addDays from 'date-fns/addDays';
import Button from '@material-ui/core/Button';

import { Typography } from '@material-ui/core';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

import Entry from './Entry';
import RequestModal from './RequestModal';
import pocData from '../../config/poc_data.json';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const SEARCH_QUERY = gql`
  query searchQuery($activities: [String], $start: String, $end: String) {
    search(activities: $activities, start: $start, end: $end) {
      id
      qualificationId
      workExperienceInYears
      activityIds
    }
  }
`;

const MATCHES_QUERY = gql`
  query {
    matches {
      id
      helper {
        id
        qualificationId
        workExperienceInYears
        activityIds
      }
      startDate
      endDate
      status
      infoText
    }
  }
`;

const PERSONNEL_REQUIREMENTS_QUERY = gql`
  query {
    personnelRequirements {
      id
      activityId
      countRequired
    }
  }
`;

const REQUEST_HELPER = gql`
  mutation requestHelper($helperId: ID, $personnelRequirementId: ID, $infoText: String) {
    requestHelper(
      helperId: $helperId
      personnelRequirementId: $personnelRequirementId
      infoText: $infoText
    ) {
      id
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
  divider: {
    marginTop: theme.spacing(3),
  },
}));

export default function Dashboard() {
  const classes = useStyles();

  // Snackbar
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('Erfolg!');

  // Modal
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState({ helperId: null });

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  };

  const [tabValue, setValue] = useState(0);
  const [filterValues, setFilterValues] = useState({});

  const [startDate, handleStartDateChange] = useState(new Date());
  const [endDate, handleEndDateChange] = useState(addDays(new Date(), 7));

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

  const { loading: requestsLoading, data: matchesData, refetch: matchesRefetch } = useQuery(
    MATCHES_QUERY,
  );

  const { data: preqsData } = useQuery(PERSONNEL_REQUIREMENTS_QUERY);

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

    if (matchesData && matchesData.matches) {
      matchesData.matches.forEach((match) => {
        if (match.status === 'Pending') {
          pending.push(match);
        } else if (match.status === 'Declined') {
          declined.push(match);
        } else if (match.status === 'Accepted') {
          // TODO needs to correctly check days
          const curDate = new Date().getTime();
          if (match.startDate < curDate && match.endDate > curDate) {
            active.push(match);
          } else {
            expired.push(match);
          }
        }
      });
    }
    setPendingRequests(pending);
    setDeclinedRequests(declined);
    setActiveRequests(active);
    setExpiredRequests(expired);
  }, [matchesData]);

  // Put PersonnelRequirements in easy to use data structure
  const [requiredActivities, setRequiredActivities] = useState([]);
  useEffect(() => {
    const currentlyRequiredActivities = [];
    if (preqsData && preqsData.personnelRequirements) {
      preqsData.personnelRequirements.forEach((preq) => {
        if (preq.countRequired > 0) currentlyRequiredActivities.push(preq.activityId);
      });
    }
    setRequiredActivities(currentlyRequiredActivities);
  }, [preqsData]);

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
                <Grid item>
                  <Typography variant="h6" color="textSecondary">
                    Helfer:
                  </Typography>
                </Grid>
                {tabValue === 0
                  && searchData
                  && searchData.search.map((searchEntry) => (
                    <Grid item key={searchEntry.id}>
                      <Entry
                        id={searchEntry.id}
                        title={pocData.qualifications[searchEntry.qualificationId].name.de}
                        workExperienceInYears={searchEntry.workExperienceInYears}
                        skills={searchEntry.activityIds.map(
                          (activityId) => pocData.activities[activityId],
                        )}
                      >
                        <Button
                          onClick={() => {
                            setModalData({
                              helperId: searchEntry.id,
                            });
                            setModalOpen(true);
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
                    <Grid item>
                      <Typography variant="subtitle1" color="secondary" gutterBottom>
                        ausstehend
                      </Typography>
                    </Grid>
                    {pendingRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pocData.qualifications[pr.helper.qualificationId].name.de}
                          skills={pr.helper.activityIds.map(
                            (activityId) => pocData.activities[activityId],
                          )}
                        ></Entry>
                      </Grid>
                    ))}
                    {pendingRequests.length === 0 && <Grid item>Keine ausstehenden Anfragen.</Grid>}

                    <Divider className={classes.divider} variant="middle" />

                    <Grid item>
                      <Typography variant="subtitle1" color="textSecondary" gutterBottom>
                        abgelehnt
                      </Typography>
                    </Grid>
                    {declinedRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pocData.qualifications[pr.helper.qualificationId].name.de}
                          skills={pr.helper.activityIds.map(
                            (activityId) => pocData.activities[activityId],
                          )}
                        ></Entry>
                      </Grid>
                    ))}
                    {declinedRequests.length === 0 && <Grid item>Keine abgelehnten Anfragen.</Grid>}
                  </>
                )}
                {tabValue === 2 && (
                  <>
                    <Grid item>
                      <Typography variant="subtitle1" color="secondary" gutterBottom>
                        aktiv
                      </Typography>
                    </Grid>
                    {activeRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pocData.qualifications[pr.helper.qualificationId].name.de}
                          skills={pr.helper.activityIds.map(
                            (activityId) => pocData.activities[activityId],
                          )}
                        ></Entry>
                      </Grid>
                    ))}
                    {activeRequests.length === 0 && <Grid item>Keine aktiven Helfer.</Grid>}

                    <Divider className={classes.divider} variant="middle" />

                    <Grid item>
                      <Typography variant="subtitle1" color="textSecondary" gutterBottom>
                        abgelaufen
                      </Typography>
                    </Grid>
                    {expiredRequests.map((pr) => (
                      <Grid item key={pr.id}>
                        <Entry
                          id={pr.id}
                          title={pocData.qualifications[pr.helper.qualificationId].name.de}
                          skills={pr.helper.activityIds.map(
                            (activityId) => pocData.activities[activityId],
                          )}
                        ></Entry>
                      </Grid>
                    ))}
                    {expiredRequests.length === 0 && <Grid item>Keine abgelaufen Helfer.</Grid>}
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

              {Object.keys(pocData.activityCategories).map((categoryId) => {
                const category = pocData.activityCategories[categoryId];

                return (
                  <React.Fragment key={categoryId}>
                    <Divider className={classes.divider} component="li" />
                    <li>
                      <Typography color="textSecondary" display="block" variant="caption">
                        {category.name.de}
                      </Typography>
                    </li>

                    {category.children
                      .filter((activityId) => requiredActivities.indexOf(activityId) !== -1)
                      .map((activityId) => (
                        <ListItem key={activityId}>
                          <FormControlLabel
                            control={
                              <Radio
                                checked={!!filterValues[activityId]}
                                name={activityId}
                                onChange={(e) => {
                                  const targetName = e.target.name;
                                  const targetChecked = e.target.checked;

                                  setFilterValues(() => ({ [targetName]: targetChecked }));
                                }}
                              />
                            }
                            label={pocData.activities[activityId].name.de}
                          />
                        </ListItem>
                      ))}
                  </React.Fragment>
                );
              })}
            </List>
            <Link to="/hospital/requirements">Bedarf anpassen?</Link>
          </Grid>
        </Grid>
      </Container>
      <RequestModal
        open={modalOpen}
        onSubmit={async (data) => {
          setModalOpen(false);

          try {
            await requestHelper({
              variables: {
                helperId: modalData.helperId,
                personnelRequirementId: preqsData.personnelRequirements.find(
                  ({ activityId }) => !!filterValues[activityId],
                ).id,
                infoText: data.infoText,
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

            matchesRefetch();
          } catch (err) {
            console.error(err);
          }
        }}
        onClose={() => setModalOpen(false)}
      />
      <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={handleSnackbarClose}>
        <Alert onClose={handleSnackbarClose} severity="success">
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </MuiPickersUtilsProvider>
  );
}
