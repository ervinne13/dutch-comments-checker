import { useState, useEffect } from 'react';
import Sheet from '@mui/joy/Sheet';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import Typography from '@mui/joy/Typography';
import Table from '@mui/joy/Table';
import Box from '@mui/joy/Box';
import Divider from '@mui/joy/Divider';
import PieChartIcon from '@mui/icons-material/PieChart';
import RefreshIcon from '@mui/icons-material/Refresh';
import IconButton from '@mui/joy/IconButton';
import { PieChart, Pie, Cell, Legend, Tooltip } from 'recharts';
import { API_BASE_URL } from './config';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const PIE_COLORS = {
  ham: '#4CAF50',
  spam: '#FFC107',
  toxic: '#F44336'
};

// Score component for color coding
function Score({ value }) {
  let color, fontWeight;
  if (value >= 0.7) {
    color = '#F44336';
    fontWeight = 'bold';
  } else if (value > 0.3) {
    color = '#FFA726';
    fontWeight = 'bold';
  } else {
    color = undefined;
    fontWeight = 'normal';
  }
  return <span style={{ color, fontWeight }}>{value}</span>;
}

// Mostly relying on Vibe-coded code. I don't really care much for the frontend, as the point of the study is on the 
// AI side of the backend, but I need something I can easily visualize.
function SubjectView() {
  const [subjects, setSubjects] = useState([]);
  const [selected, setSelected] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [expandedRows, setExpandedRows] = useState({});

  const fetchSubjects = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/subjects`);
      const data = await res.json();
      setSubjects(data);
      setSelected(data[0] || null);
    } catch (err) {
      setError('Failed to load subjects');
    }
    setLoading(false);
  };

  const fetchComments = async (subjectId) => {
    setCommentsLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/subjects/${subjectId}/comments`);
      const data = await res.json();
      setComments(data);
    } catch (err) {
      setComments([]);
    }
    setCommentsLoading(false);
  };

  useEffect(() => {
    fetchSubjects();
  }, []);

  useEffect(() => {
    if (selected) {
      fetchComments(selected.id);
    }
  }, [selected]);

  const toggleRow = (id) => {
    setExpandedRows(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // Pie chart data
  const spamData = selected ? [
    { name: 'Spam', value: selected.spam_count || 0, color: PIE_COLORS.spam },
    { name: 'OK', value: (selected.comment_count || 0) - (selected.spam_count || 0), color: PIE_COLORS.ham }
  ] : [];
  const toxicData = selected ? [
    { name: 'Toxic', value: selected.toxic_count || 0, color: PIE_COLORS.toxic },
    { name: 'OK', value: (selected.comment_count || 0) - (selected.toxic_count || 0), color: PIE_COLORS.ham }
  ] : [];

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* Left: Subject List */}
      <Sheet variant="soft" sx={{ width: 300, p: 2, borderRight: '1px solid #eee' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Typography level="h4" sx={{ flexGrow: 1 }}>Moderate by Subject</Typography>
          <IconButton size="sm" sx={{ ml: 1 }} onClick={fetchSubjects} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Box>
        <Typography level="h5" sx={{ mb: 2 }}>Recent Subjects</Typography>
        {loading ? (
          <Typography level="body-md">Loading...</Typography>
        ) : error ? (
          <Typography level="body-md" color="danger">{error}</Typography>
        ) : (
          <List>
            {subjects.map(subj => (
              <ListItem key={subj.id} selected={selected && selected.id === subj.id} onClick={() => setSelected(subj)} sx={{ cursor: 'pointer' }}>
                <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                  <Typography level="title-md">{subj.title}</Typography>
                  <Typography level="body-sm">Comments: {subj.comment_count} | Spam: {subj.spam_count} | Toxic: {subj.toxic_count}</Typography>
                </Box>
              </ListItem>
            ))}
          </List>
        )}
      </Sheet>
      {/* Right: Subject Details */}
      <Box sx={{ flex: 1, p: 3 }}>
        {selected ? (
          <>
            <Typography level="h2" sx={{ mb: 2 }}>{selected.title}</Typography>
            <Box sx={{ display: 'flex', gap: 4, mb: 4 }}>
              <Box>
                <Typography level="title-md" sx={{ mb: 1 }}><PieChartIcon fontSize="small" /> Spam</Typography>
                <PieChart width={180} height={180}>
                  <Pie data={spamData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} label>
                    {spamData.map((entry, idx) => (
                      <Cell key={`cell-spam-${idx}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Legend />
                  <Tooltip />
                </PieChart>
              </Box>
              <Box>
                <Typography level="title-md" sx={{ mb: 1 }}><PieChartIcon fontSize="small" /> Toxicity</Typography>
                <PieChart width={180} height={180}>
                  <Pie data={toxicData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} label>
                    {toxicData.map((entry, idx) => (
                      <Cell key={`cell-toxic-${idx}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Legend />
                  <Tooltip />
                </PieChart>
              </Box>
            </Box>
            <Divider sx={{ mb: 2 }} />
            <Typography level="h4" sx={{ mb: 1 }}>Comments</Typography>
            {commentsLoading ? (
              <Typography level="body-md">Loading comments...</Typography>
            ) : (
              <>
                <Table variant="soft" borderAxis="xBetween" sx={{ minWidth: 600 }}>
                  <thead>
                    <tr>
                      <th style={{ width: '80%' }}>Comment Text</th>
                      <th>Spam</th>
                      <th>Toxic</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {comments.map((c, idx) => (
                      <>
                        <tr key={c.id || idx}>
                          <td style={{ width: '80%' }}>{c.text}</td>
                          <td><Score value={c.spam} /></td>
                          <td><Score value={c.toxic} /></td>
                          <td>
                            <IconButton size="sm" onClick={() => toggleRow(c.id)}>
                              {expandedRows[c.id] ? <ExpandMoreIcon /> : <ChevronRightIcon />}
                            </IconButton>
                          </td>
                        </tr>
                        {expandedRows[c.id] && (
                          <tr>
                            <td colSpan={4}>
                              <Box sx={{ p: 2, bgcolor: '#f9f9f9', borderRadius: 2 }}>
                                <Table size="sm" sx={{ mt: 2, minWidth: 600 }}>
                                  <thead>
                                    <tr>
                                      <th>Spam</th>
                                      <th>Ham</th>
                                      <th>Toxic</th>
                                      <th>Insult</th>
                                      <th>Obscene</th>
                                      <th>Identity Hate</th>
                                      <th>Severe Toxic</th>
                                      <th>Threat</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    <tr>
                                      {[c.spam, c.ham, c.toxic, c.insult, c.obscene, c.identity_hate, c.severe_toxic, c.threat].map((score, i) => (
                                        <td key={i} style={{ color: score >= 0.7 ? '#F44336' : score > 0.3 ? '#FFA726' : undefined, fontWeight: score > 0.3 ? 'bold' : 'normal' }}>
                                          {score}
                                        </td>
                                      ))}
                                    </tr>
                                  </tbody>
                                </Table>

                                <Box sx={{ mb: 2 }}>
                                  <Typography level="body-md"><b>Translation:</b></Typography>
                                  <Typography level="body-md"  sx={{ mb: 1 }}>{c.text_translation}</Typography>
                                  {(c.spam > 0.3 || c.toxic > 0.3) && (
                                    <>
                                      <Typography level="body-md"><b>Llama3 Remarks:</b></Typography>
                                      <Typography level="body-md" sx={{ mb: 1 }}>{c.reasoning}</Typography>
                                      <Typography level="body-md"><b>Recommended Action:</b> {c.recommended_action}</Typography>
                                      <Typography level="body-md"><b>Confidence:</b> {c.confidence}</Typography>
                                    </>
                                  )}
                                </Box>

                                {(c.spam > 0.3 || c.toxic > 0.3) && (
                                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 2 }}>
                                    <IconButton variant="soft" color="warning" size="md" sx={{ px: 2 }}>
                                      Disagree with LLM Decision (Restore Comment)
                                    </IconButton>
                                    <IconButton variant="soft" color="danger" size="md" sx={{ px: 2 }}>
                                      Mute User
                                    </IconButton>
                                  </Box>
                                )}
                            </Box>
                          </td>
                        </tr>
                      )}
                    </>
                  ))}
                </tbody>
              </Table>
              </>
            )}
          </>
        ) : (
          <Typography level="h3">Select a subject to view details</Typography>
        )}
      </Box>
    </Box>
  );
}

function App() {
  return <SubjectView />;
}

export default App;
