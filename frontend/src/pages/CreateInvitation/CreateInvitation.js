import {
  Box,
  Button,
  Container,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemSecondaryAction,
  ListItemText,
  ListSubheader,
  Paper,
  Switch,
  TextField,
} from '@material-ui/core';
import { ExpandMore, ChevronRight } from '@material-ui/icons';
import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@apollo/react-hooks';
import { gql } from 'apollo-boost';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const PERSONNEL_REQUIREMENTS_QUERY = gql`
  query {
    personnelRequirements {
      id
      activityId
      countRequired
    }
  }
`;

const SET_PERSONNEL_REQUIREMENT = gql`
  mutation setPersonnelRequirement($activityId: String, $countRequired: Int) {
    setPersonnelRequirement(activityId: $activityId, countRequired: $countRequired) {
      id
    }
  }
`;

const CreateInvitationPage = () => {
  const [enabledLines, setEnabledLines] = useState([]);
  const [countValues, setCountValues] = useState({});

  const { data } = useQuery(PERSONNEL_REQUIREMENTS_QUERY);

  const [setPersonnelRequirement] = useMutation(SET_PERSONNEL_REQUIREMENT);

  // Snackbar
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('Erfolg!');

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  };

  useEffect(() => {
    const currentCountValues = {};
    if (data && data.personnelRequirements) {
      data.personnelRequirements.forEach((preq) => {
        currentCountValues[preq.activityId] = preq.countRequired;
      });
    }
    setCountValues(currentCountValues);
  }, [data]);

  const dropdownIndex = 'medical-1';

  const isLineEnabled = (index) => enabledLines.indexOf(index) !== -1 || countValues[index] > 0;

  const toggleLine = (index) => {
    const lines = enabledLines.slice(0);

    if (isLineEnabled(index)) {
      lines.splice(lines.indexOf(index), 1);
      setEnabledLines(lines);
      return;
    }

    lines.push(index);
    setEnabledLines(lines);
  };

  const showDropdown = true;

  return (
    <div className="py center-vertical">
      <Container>
        <Paper className="paper--content-wrapper max-w-4xl m-auto">
          <h1>Ausschreibung erstellen</h1>

          <Divider />

          <h2>Bedarf wählen</h2>

          <form noValidate autoComplete="off">
            {/* SECTION: Administration */}
            <List subheader={<ListSubheader>Administration</ListSubheader>}>
              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('ad-a');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('ad-a')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Personalabteilung/HR" />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['ad-a'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'ad-a': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('ad-a')}
                  />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('ad-b');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('ad-b')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Kommunikation" />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['ad-b'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'ad-b': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('ad-b')}
                  />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('ad-c');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('ad-c')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="IT-Unterstützung" />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['ad-c'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'ad-c': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('ad-c')}
                  />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('ad-d');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('ad-d')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Buchhaltung" />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['ad-d'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'ad-d': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('ad-d')}
                  />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('ad-e');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('ad-e')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Rechtsabteilung" />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['ad-e'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'ad-e': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('ad-e')}
                  />
                </ListItemSecondaryAction>
              </ListItem>
            </List>

            <Divider />

            {/* SECTION: Logistik */}
            <List subheader={<ListSubheader>Logistik</ListSubheader>}>
              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('lo-a');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('lo-a')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText
                  id={'switch-list-label-wifi'}
                  primary="Planung, Materialbeschaffung"
                />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['lo-a'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'lo-a': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('lo-a')}
                  />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('lo-b');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('lo-b')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText
                  id={'switch-list-label-wifi'}
                  primary="logistische Hilfsarbeiten, wie Krankentransport, Bluttransport, RTW"
                />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['lo-b'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'lo-b': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('lo-b')}
                  />
                </ListItemSecondaryAction>
              </ListItem>
            </List>

            <Divider />

            {/* SECTION: Medizin */}
            <List subheader={<ListSubheader>Medizin</ListSubheader>}>
              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine(dropdownIndex);
                }}
              >
                <ListItemText
                  id={'switch-list-label-wifi'}
                  primary="Direkte Versorgung am Patienten"
                />
                <ListItemSecondaryAction>
                  <IconButton aria-label="expand dropdown" size="small" disabled={true}>
                    <ExpandMore />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>

              {showDropdown && (
                <div className="mx-4">
                  <List>
                    <ListItem
                      role={undefined}
                      dense
                      button
                      disableRipple
                      onClick={() => {
                        toggleLine('me-a-1');
                      }}
                    >
                      <ListItemIcon>
                        <Switch
                          edge="start"
                          checked={isLineEnabled('me-a-1')}
                          tabIndex={-1}
                          inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        id={'switch-list-label-wifi'}
                        primary="Beratung (Hotline/Mail)"
                      />
                      <ListItemSecondaryAction>
                        <TextField
                          value={countValues['me-a-1'] || 0}
                          onChange={(e) => {
                            const { value } = e.target;
                            setCountValues((state) => ({ ...state, 'me-a-1': value }));
                          }}
                          edge="end"
                          id="standard-basic"
                          label="Anzahl Personen"
                          type="number"
                          variant="outlined"
                          size="small"
                          disabled={!isLineEnabled('me-a-1')}
                        />
                      </ListItemSecondaryAction>
                    </ListItem>

                    <ListItem
                      role={undefined}
                      dense
                      button
                      disableRipple
                      onClick={() => {
                        toggleLine('me-a-2');
                      }}
                    >
                      <ListItemIcon>
                        <Switch
                          edge="start"
                          checked={isLineEnabled('me-a-2')}
                          tabIndex={-1}
                          inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        id={'switch-list-label-wifi'}
                        primary="Aufnahmebereich PatientInnen"
                      />
                      <ListItemSecondaryAction>
                        <TextField
                          value={countValues['me-a-2'] || 0}
                          onChange={(e) => {
                            const { value } = e.target;
                            setCountValues((state) => ({ ...state, 'me-a-2': value }));
                          }}
                          edge="end"
                          id="standard-basic"
                          label="Anzahl Personen"
                          type="number"
                          variant="outlined"
                          size="small"
                          disabled={!isLineEnabled('me-a-2')}
                        />
                      </ListItemSecondaryAction>
                    </ListItem>

                    <ListItem
                      role={undefined}
                      dense
                      button
                      disableRipple
                      onClick={() => {
                        toggleLine('me-a-3');
                      }}
                    >
                      <ListItemIcon>
                        <Switch
                          edge="start"
                          checked={isLineEnabled('me-a-3')}
                          tabIndex={-1}
                          inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        id={'switch-list-label-wifi'}
                        primary="Bereich Normalstation - Pflege"
                      />
                      <ListItemSecondaryAction>
                        <TextField
                          value={countValues['me-a-3'] || 0}
                          onChange={(e) => {
                            const { value } = e.target;
                            setCountValues((state) => ({ ...state, 'me-a-3': value }));
                          }}
                          edge="end"
                          id="standard-basic"
                          label="Anzahl Personen"
                          type="number"
                          variant="outlined"
                          size="small"
                          disabled={!isLineEnabled('me-a-3')}
                        />
                      </ListItemSecondaryAction>
                    </ListItem>

                    <ListItem
                      role={undefined}
                      dense
                      button
                      disableRipple
                      onClick={() => {
                        toggleLine('me-a-4');
                      }}
                    >
                      <ListItemIcon>
                        <Switch
                          edge="start"
                          checked={isLineEnabled('me-a-4')}
                          tabIndex={-1}
                          inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        id={'switch-list-label-wifi'}
                        primary="Bereich Intensivstation/IMC – Pflege"
                      />
                      <ListItemSecondaryAction>
                        <TextField
                          value={countValues['me-a-4'] || 0}
                          onChange={(e) => {
                            const { value } = e.target;
                            setCountValues((state) => ({ ...state, 'me-a-4': value }));
                          }}
                          edge="end"
                          id="standard-basic"
                          label="Anzahl Personen"
                          type="number"
                          variant="outlined"
                          size="small"
                          disabled={!isLineEnabled('me-a-4')}
                        />
                      </ListItemSecondaryAction>
                    </ListItem>

                    <ListItem
                      role={undefined}
                      dense
                      button
                      disableRipple
                      onClick={() => {
                        toggleLine('me-a-5');
                      }}
                    >
                      <ListItemIcon>
                        <Switch
                          edge="start"
                          checked={isLineEnabled('me-a-5')}
                          tabIndex={-1}
                          inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        id={'switch-list-label-wifi'}
                        primary="Bereich Intensivstation ohne Beatmung - medizinische Versorgung"
                      />
                      <ListItemSecondaryAction>
                        <TextField
                          value={countValues['me-a-5'] || 0}
                          onChange={(e) => {
                            const { value } = e.target;
                            setCountValues((state) => ({ ...state, 'me-a-5': value }));
                          }}
                          edge="end"
                          id="standard-basic"
                          label="Anzahl Personen"
                          type="number"
                          variant="outlined"
                          size="small"
                          disabled={!isLineEnabled('me-a-5')}
                        />
                      </ListItemSecondaryAction>
                    </ListItem>

                    <ListItem
                      role={undefined}
                      dense
                      button
                      disableRipple
                      onClick={() => {
                        toggleLine('me-a-6');
                      }}
                    >
                      <ListItemIcon>
                        <Switch
                          edge="start"
                          checked={isLineEnabled('me-a-6')}
                          tabIndex={-1}
                          inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        id={'switch-list-label-wifi'}
                        primary="Bereich Intensivstation mit Beatmung - medizinische Versorgung"
                      />
                      <ListItemSecondaryAction>
                        <TextField
                          value={countValues['me-a-6'] || 0}
                          onChange={(e) => {
                            const { value } = e.target;
                            setCountValues((state) => ({ ...state, 'me-a-6': value }));
                          }}
                          edge="end"
                          id="standard-basic"
                          label="Anzahl Personen"
                          type="number"
                          variant="outlined"
                          size="small"
                          disabled={!isLineEnabled('me-a-6')}
                        />
                      </ListItemSecondaryAction>
                    </ListItem>

                    <ListItem
                      role={undefined}
                      dense
                      button
                      disableRipple
                      onClick={() => {
                        toggleLine('me-a-7');
                      }}
                    >
                      <ListItemIcon>
                        <Switch
                          edge="start"
                          checked={isLineEnabled('me-a-7')}
                          tabIndex={-1}
                          inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        id={'switch-list-label-wifi'}
                        primary="Beatmung verändern [Assistenzarzt/Facharzt]"
                      />
                      <ListItemSecondaryAction>
                        <TextField
                          value={countValues['me-a-7'] || 0}
                          onChange={(e) => {
                            const { value } = e.target;
                            setCountValues((state) => ({ ...state, 'me-a-7': value }));
                          }}
                          edge="end"
                          id="standard-basic"
                          label="Anzahl Personen"
                          type="number"
                          variant="outlined"
                          size="small"
                          disabled={!isLineEnabled('me-a-7')}
                        />
                      </ListItemSecondaryAction>
                    </ListItem>
                  </List>
                </div>
              )}

              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('me-b');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('me-b')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText
                  id={'switch-list-label-wifi'}
                  primary="Operativer Tätigkeitsbereich"
                />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['me-b'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'me-b': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('me-b')}
                  />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem
                role={undefined}
                dense
                button
                disableRipple
                onClick={() => {
                  toggleLine('me-c');
                }}
              >
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('me-c')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText
                  id={'switch-list-label-wifi'}
                  primary="Weitere Tätigkeitsbereiche mit med. Vorausbildung (Physios, MTAs, ...)"
                />
                <ListItemSecondaryAction>
                  <TextField
                    value={countValues['me-c'] || 0}
                    onChange={(e) => {
                      const { value } = e.target;
                      setCountValues((state) => ({ ...state, 'me-c': value }));
                    }}
                    edge="end"
                    id="standard-basic"
                    label="Anzahl Personen"
                    type="number"
                    variant="outlined"
                    size="small"
                    disabled={!isLineEnabled('me-c')}
                  />
                </ListItemSecondaryAction>
              </ListItem>
            </List>

            <Box className="mt-6">
              {/* Abort */}
              <Button variant="contained">Abbrechen</Button>

              {/* Submit */}
              <Button
                variant="contained"
                color="primary"
                className="float-right"
                type="submit"
                endIcon={<ChevronRight />}
                onClick={async (e) => {
                  e.preventDefault();
                  try {
                    const allUpdates = [];

                    Object.entries(countValues).forEach(([key, value]) => {
                      allUpdates.push(
                        setPersonnelRequirement({
                          variables: {
                            activityId: key,
                            countRequired: value,
                          },
                        }),
                      );
                    });

                    setSnackbarMessage('Bedarf erfolgreich gespeichert!');
                    setSnackbarOpen(true);

                    await Promise.all(allUpdates);
                  } catch (err) {
                    console.error(err);
                  }
                }}
              >
                Speichern
              </Button>
            </Box>
          </form>
        </Paper>
      </Container>
      <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={handleSnackbarClose}>
        <Alert onClose={handleSnackbarClose} severity="success">
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default CreateInvitationPage;
