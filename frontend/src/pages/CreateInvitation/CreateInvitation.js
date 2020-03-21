import {
  Box,
  Button,
  Container,
  Divider,
  ExpansionPanel,
  ExpansionPanelDetails,
  ExpansionPanelSummary,
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
  Typography,
} from '@material-ui/core';
import { ExpandMore, ChevronRight } from '@material-ui/icons';
import React, { useState } from 'react';

const CreateInvitationPage = () => {
  const [enabledLines, setEnabledLines] = useState([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const dropdownIndex = 'medical-1';

  const isLineEnabled = (index) => enabledLines.indexOf(index) !== -1;

  const toggleLine = (index) => {
    const lines = enabledLines.slice(0);

    if (isLineEnabled(index)) {
      lines.splice(lines.indexOf(index), 1);
      setEnabledLines(lines);
      return;
    }

    if (index === dropdownIndex) {
      setIsDropdownOpen(true);
    }

    lines.push(index);
    setEnabledLines(lines);
  };

  const showDropdown = isLineEnabled('medical-1') && isDropdownOpen === true;

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

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('admin-1'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('admin-1')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Personalabteilung/HR" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('admin-1')} />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('admin-2'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('admin-2')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Kommunikation" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('admin-2')} />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('admin-3'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('admin-3')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="IT-Unterstützung, um Helfer kurz zu briefen" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('admin-3')} />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('admin-4'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('admin-4')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Buchhaltung" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('admin-4')} />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('admin-5'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('admin-5')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Rechtsabteilung" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('admin-5')} />
                </ListItemSecondaryAction>
              </ListItem>
            </List>

            <Divider />

            {/* SECTION: Logistik */}
            <List subheader={<ListSubheader>Logistik</ListSubheader>}>
              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('logistic-1'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('logistic-1')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Planung, Materialbeschaffung" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('logistic-1')} />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('logistic-2'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('logistic-2')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="logistische Hilfsarbeiten, wie Krankentransport, Bluttransport, RTW" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('logistic-2')} />
                </ListItemSecondaryAction>
              </ListItem>
            </List>

            <Divider />

            {/* SECTION: Medizin */}
            <List subheader={<ListSubheader>Medizin</ListSubheader>}>
              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine(dropdownIndex); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled(dropdownIndex)}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Direkte Versorgung am Patienten" />
                <ListItemSecondaryAction>
                  <IconButton aria-label="expand dropdown" size="small" disabled={!isLineEnabled(dropdownIndex)} onClick={() => { setIsDropdownOpen(!isDropdownOpen); }}>
                    <ExpandMore />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>

              {showDropdown
                && (
                  <div className="mx-4">
                    <List>
                      <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-1-1'); }}>
                        <ListItemIcon>
                          <Switch
                            edge="start"
                            checked={isLineEnabled('medical-1-1')}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                          />
                        </ListItemIcon>
                        <ListItemText id={'switch-list-label-wifi'} primary="Beratung (Hotline/Mail)" />
                        <ListItemSecondaryAction>
                          <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-1-1')} />
                        </ListItemSecondaryAction>
                      </ListItem>

                      <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-1-2'); }}>
                        <ListItemIcon>
                          <Switch
                            edge="start"
                            checked={isLineEnabled('medical-1-2')}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                          />
                        </ListItemIcon>
                        <ListItemText id={'switch-list-label-wifi'} primary="Aufnahmebereich PatientInnen" />
                        <ListItemSecondaryAction>
                          <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-1-2')} />
                        </ListItemSecondaryAction>
                      </ListItem>

                      <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-1-3'); }}>
                        <ListItemIcon>
                          <Switch
                            edge="start"
                            checked={isLineEnabled('medical-1-3')}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                          />
                        </ListItemIcon>
                        <ListItemText id={'switch-list-label-wifi'} primary="Bereich Normalstation - Pflege" />
                        <ListItemSecondaryAction>
                          <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-1-3')} />
                        </ListItemSecondaryAction>
                      </ListItem>

                      <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-1-4'); }}>
                        <ListItemIcon>
                          <Switch
                            edge="start"
                            checked={isLineEnabled('medical-1-4')}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                          />
                        </ListItemIcon>
                        <ListItemText id={'switch-list-label-wifi'} primary="Bereich Intensivstation/IMC – Pflege" />
                        <ListItemSecondaryAction>
                          <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-1-4')} />
                        </ListItemSecondaryAction>
                      </ListItem>

                      <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-1-5'); }}>
                        <ListItemIcon>
                          <Switch
                            edge="start"
                            checked={isLineEnabled('medical-1-5')}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                          />
                        </ListItemIcon>
                        <ListItemText id={'switch-list-label-wifi'} primary="Bereich Intensivstation ohne Beatmung - medizinische Versorgung" />
                        <ListItemSecondaryAction>
                          <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-1-5')} />
                        </ListItemSecondaryAction>
                      </ListItem>

                      <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-1-6'); }}>
                        <ListItemIcon>
                          <Switch
                            edge="start"
                            checked={isLineEnabled('medical-1-6')}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                          />
                        </ListItemIcon>
                        <ListItemText id={'switch-list-label-wifi'} primary="Bereich Intensivstation mit Beatmung - medizinische Versorgung" />
                        <ListItemSecondaryAction>
                          <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-1-6')} />
                        </ListItemSecondaryAction>
                      </ListItem>

                      <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-1-7'); }}>
                        <ListItemIcon>
                          <Switch
                            edge="start"
                            checked={isLineEnabled('medical-1-7')}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                          />
                        </ListItemIcon>
                        <ListItemText id={'switch-list-label-wifi'} primary="Beatmung verändern [Assistenzarzt/Facharzt]" />
                        <ListItemSecondaryAction>
                          <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-1-7')} />
                        </ListItemSecondaryAction>
                      </ListItem>
                    </List>
                  </div>
                )
              }

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-2'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('medical-2')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Operativer Tätigkeitsbereich" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-2')} />
                </ListItemSecondaryAction>
              </ListItem>

              <ListItem role={undefined} dense button disableRipple onClick={() => { toggleLine('medical-3'); }}>
                <ListItemIcon>
                  <Switch
                    edge="start"
                    checked={isLineEnabled('medical-3')}
                    tabIndex={-1}
                    inputProps={{ 'aria-labelledby': 'switch-list-label-wifi' }}
                  />
                </ListItemIcon>
                <ListItemText id={'switch-list-label-wifi'} primary="Weitere Tätigkeitsbereiche mit med. Vorausbildung (Physios, MTAs, ...)" />
                <ListItemSecondaryAction>
                  <TextField edge="end" id="standard-basic" label="Anzahl Personen" type="number" variant="outlined" size="small" disabled={!isLineEnabled('medical-3')} />
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
              >
                Weiter
              </Button>
            </Box>
          </form>
        </Paper>
      </Container>
    </div>
  );
};

export default CreateInvitationPage;
