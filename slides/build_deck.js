const pptxgen = require("pptxgenjs");

const INK = "1C1B22", BERRY = "B5446E", GREEN = "4C9F70", AMBER = "D98C2B";
const PAPER = "FFFFFF", MUTE = "6B6B76", WASH = "F4F2F5", LINE = "DEDAE1";
const H = "Cambria", B = "Calibri", M = "Courier New";

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";              // 13.3 x 7.5
p.author = "Workshop";
p.title = "Coding with AI";

const W = 13.33, PAD = 0.85;

function dark(title, sub, notes) {
  const s = p.addSlide();
  s.background = { color: INK };
  s.addText(title, { x: PAD, y: 2.5, w: W - 2 * PAD, h: 1.5, fontSize: 46, bold: true,
    color: PAPER, fontFace: H });
  if (sub) s.addText(sub, { x: PAD, y: 4.0, w: W - 2 * PAD, h: 1.6, fontSize: 20,
    color: "C8C2CE", fontFace: B, lineSpacing: 30 });
  if (notes) s.addNotes(notes);
  return s;
}

function light(title, notes) {
  const s = p.addSlide();
  s.background = { color: PAPER };
  s.addText(title, { x: PAD, y: 0.5, w: W - 2 * PAD, h: 0.9, fontSize: 34, bold: true,
    color: INK, fontFace: H, margin: 0 });
  if (notes) s.addNotes(notes);
  return s;
}

function card(s, x, y, w, h, fill) {
  s.addShape(p.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.09,
    fill: { color: fill || WASH }, line: { color: LINE, width: 1 } });
}

function numDot(s, x, y, n, color) {
  s.addShape(p.ShapeType.ellipse, { x, y, w: 0.42, h: 0.42, fill: { color } });
  s.addText(String(n), { x, y, w: 0.42, h: 0.42, fontSize: 14, bold: true,
    color: PAPER, align: "center", valign: "middle", fontFace: B, margin: 0 });
}

/* ---------------------------------------------------------------- 1 title */
dark("Coding with AI",
  "Python and R for people who don't code\n\nA hands-on workshop  ·  3 hours  ·  nothing to install",
  "Welcome. Three tabs open: your AI, Colab, Posit Cloud. Don't start until everyone's in.");

/* ---------------------------------------------------------------- 2 thesis */
{
  const s = p.addSlide();
  s.background = { color: INK };
  s.addText("The bottleneck was never typing.", { x: PAD, y: 2.0, w: W - 2 * PAD, h: 0.9,
    fontSize: 40, bold: true, color: PAPER, fontFace: H });
  s.addText("It was knowing what to type.", { x: PAD, y: 2.95, w: W - 2 * PAD, h: 0.9,
    fontSize: 40, bold: true, color: BERRY, fontFace: H });
  s.addText("AI removes the typing.\nIt does not remove the knowing — it just makes it possible to skip the knowing without noticing that you did.",
    { x: PAD, y: 4.3, w: 10.2, h: 1.6, fontSize: 19, color: "C8C2CE", fontFace: B, lineSpacing: 30 });
  s.addNotes("Say this out loud. Repeat it at the end. Everything today serves this line.");
}

/* ---------------------------------------------------------------- 3 build */
{
  const s = light("What you'll walk out with", "Three things. The third is the real one.");
  const items = [
    [GREEN, "An NLP pipeline", "Turn 60 picture-description transcripts into quantitative language measures.", "Python · pandas · spaCy · scikit-learn"],
    [BERRY, "A model and a figure", "Predict aphasia severity from language. Make a plot you'd put in a paper.", "R · dplyr · lme4 · ggplot2"],
    [AMBER, "A working BS detector", "The ability to tell when your assistant is quietly, fluently wrong.", "The part that actually matters"],
  ];
  items.forEach(([c, t, d, tech], i) => {
    const x = PAD + i * 4.0;
    card(s, x, 1.75, 3.6, 3.9);
    s.addShape(p.ShapeType.ellipse, { x: x + 0.32, y: 2.1, w: 0.5, h: 0.5, fill: { color: c } });
    s.addText(t, { x: x + 0.32, y: 2.8, w: 3.0, h: 0.5, fontSize: 19, bold: true, color: INK, fontFace: H, margin: 0 });
    s.addText(d, { x: x + 0.32, y: 3.35, w: 2.96, h: 1.5, fontSize: 14, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 20 });
    s.addText(tech, { x: x + 0.32, y: 4.95, w: 2.96, h: 0.5, fontSize: 11, italic: true, color: MUTE, fontFace: B, margin: 0 });
  });
  s.addText("You will not type much code today. That is the point.",
    { x: PAD, y: 6.05, w: 11.6, h: 0.5, fontSize: 16, italic: true, color: BERRY, fontFace: B, margin: 0 });
}

/* ---------------------------------------------------------------- 4 tabs */
{
  const s = light("Three tabs. That's the whole setup.", "Setup triage. Do not proceed until every laptop is in all three.");
  const rows = [
    [BERRY, "Your AI assistant", "claude.ai — or ChatGPT, or whatever your institution gives you. Free tier is fine."],
    [GREEN, "Google Colab", "Python in the browser. colab.research.google.com. Nothing installs on your machine."],
    [AMBER, "Posit Cloud", "RStudio in the browser. posit.cloud. Click SAVE A PERMANENT COPY or you lose your work."],
  ];
  rows.forEach(([c, t, d], i) => {
    const y = 1.85 + i * 1.4;
    numDot(s, PAD, y + 0.16, i + 1, c);
    s.addText(t, { x: PAD + 0.72, y: y, w: 3.3, h: 0.42, fontSize: 18, bold: true, color: INK, fontFace: H, margin: 0 });
    s.addText(d, { x: PAD + 0.72, y: y + 0.46, w: 9.5, h: 0.6, fontSize: 14, color: "3A3A44", fontFace: B, margin: 0 });
  });
  card(s, PAD, 6.05, 11.6, 0.85, "FBF0F4");
  s.addText("Today's data is 100% synthetic. Generated by a script. Nobody's health information is anywhere in this room.",
    { x: PAD + 0.3, y: 6.05, w: 11.0, h: 0.85, fontSize: 14, bold: true, color: BERRY, fontFace: B, valign: "middle", margin: 0 });
}

/* ---------------------------------------------------------------- 5 what it is */
{
  const s = light("What is actually happening when it writes code", "Not a lecture. Two minutes. But they need the mental model.");
  card(s, PAD, 1.7, 5.6, 4.2, "F1F7F3");
  s.addText("What it IS doing", { x: PAD + 0.35, y: 1.95, w: 5.0, h: 0.4, fontSize: 17, bold: true, color: GREEN, fontFace: H, margin: 0 });
  s.addText([
    { text: "Predicting the next token, given everything before it", options: { bullet: true, breakLine: true } },
    { text: "Trained on essentially all public code and documentation", options: { bullet: true, breakLine: true } },
    { text: "Extremely good at the shape of a correct answer", options: { bullet: true, breakLine: true } },
    { text: "Genuinely useful, most of the time", options: { bullet: true } },
  ], { x: PAD + 0.35, y: 2.5, w: 5.0, h: 3.2, fontSize: 14, color: "3A3A44", fontFace: B, paraSpaceAfter: 10, margin: 0 });

  card(s, PAD + 6.0, 1.7, 5.6, 4.2, "FBF0F4");
  s.addText("What it is NOT doing", { x: PAD + 6.35, y: 1.95, w: 5.0, h: 0.4, fontSize: 17, bold: true, color: BERRY, fontFace: H, margin: 0 });
  s.addText([
    { text: "Running your code", options: { bullet: true, breakLine: true } },
    { text: "Looking at your data", options: { bullet: true, breakLine: true } },
    { text: "Knowing your study design", options: { bullet: true, breakLine: true } },
    { text: "Checking whether the answer is true", options: { bullet: true } },
  ], { x: PAD + 6.35, y: 2.5, w: 5.0, h: 3.2, fontSize: 14, color: "3A3A44", fontFace: B, paraSpaceAfter: 10, margin: 0 });

  s.addText("So: fast, fluent, confident — and with no idea whether it's right. Exactly like a very well-read first-year grad student who will never, ever say \"I don't know.\"",
    { x: PAD, y: 6.1, w: 11.6, h: 0.8, fontSize: 15, italic: true, color: INK, fontFace: B, margin: 0, lineSpacing: 22 });
}

/* ---------------------------------------------------------------- 6 recipe */
{
  const s = light("A bad prompt is a wish. A good prompt is a brief.", "The core teaching slide of block 1. Then demo the bad prompt live.");
  const rows = [
    ["Who you are", "\"I'm a researcher using R in RStudio. I'm a beginner.\""],
    ["What the data is", "\"A CSV at data/x.csv, columns: id, group, age, wab_aq, transcript\""],
    ["The ONE task", "\"Fit a linear model predicting wab_aq from age.\""],
    ["The constraints", "\"Use dplyr. Don't install anything new.\""],
    ["The output you want", "\"Just the code with short comments. No explanation.\""],
  ];
  rows.forEach(([k, v], i) => {
    const y = 1.75 + i * 0.92;
    card(s, PAD, y, 11.6, 0.78, i % 2 ? WASH : PAPER);
    numDot(s, PAD + 0.22, y + 0.18, i + 1, BERRY);
    s.addText(k, { x: PAD + 0.85, y: y, w: 2.6, h: 0.78, fontSize: 15, bold: true, color: INK, fontFace: B, valign: "middle", margin: 0 });
    s.addText(v, { x: PAD + 3.55, y: y, w: 7.8, h: 0.78, fontSize: 13, color: "3A3A44", fontFace: M, valign: "middle", margin: 0 });
  });
  s.addText("Paste your REAL column names. Every hallucinated variable traces back to an AI guessing at a structure you never showed it.",
    { x: PAD, y: 6.45, w: 11.6, h: 0.5, fontSize: 14, bold: true, color: BERRY, fontFace: B, margin: 0 });
}

/* ---------------------------------------------------------------- 7 debug loop */
{
  const s = light("The debugging loop is not failure. It's the job.", "Normalise this hard. Beginners think an error means they broke it.");
  const steps = [
    ["Paste the whole error", "All of it. The traceback, the line numbers, the warning you skipped. Not your summary of it."],
    ["Paste the whole code", "Not the line you think is broken. The block. It cannot see your screen."],
    ["Say what you're running", "\"R 4.4, tidyverse 2.0.\" Half of all errors are version errors."],
  ];
  steps.forEach(([t, d], i) => {
    const x = PAD + i * 4.0;
    card(s, x, 1.8, 3.6, 2.9);
    numDot(s, x + 0.3, 2.1, i + 1, GREEN);
    s.addText(t, { x: x + 0.3, y: 2.65, w: 3.0, h: 0.5, fontSize: 16, bold: true, color: INK, fontFace: H, margin: 0 });
    s.addText(d, { x: x + 0.3, y: 3.2, w: 3.0, h: 1.3, fontSize: 13, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 18 });
  });
  card(s, PAD, 5.1, 11.6, 1.55, "FDF6EC");
  s.addText("The three-strikes rule", { x: PAD + 0.4, y: 5.25, w: 5.0, h: 0.4, fontSize: 16, bold: true, color: AMBER, fontFace: H, margin: 0 });
  s.addText("Three failures on the same error means it's stuck in a groove. Open a NEW chat. Describe the goal from scratch. Do not paste the failed attempts. Fresh context beats more argument.",
    { x: PAD + 0.4, y: 5.7, w: 10.8, h: 0.8, fontSize: 14, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 20 });
}

/* ---------------------------------------------------------------- 8 DEMO */
dark("Live demo",
  "1.  \"write me some code to analyse my data\"\n\n2.  \"I have 30 patients measured twice. Did they improve? Give me the R code.\"\n\nThen ask it:  \"Are you sure? What are you assuming about independence?\"",
  "Demo 1: it invents everything. Nobody's fault — you asked for nothing.\n\nDemo 2: watch it change its answer under questioning. THE LINE: 'It knew. It always knew. It just doesn't lead with it. That gap is where your career gets damaged.'");

/* ---------------------------------------------------------------- 9 PART 1 */
dark("Part 1 — Python", "Turning transcripts into numbers\n\n45 minutes  ·  01_python_starter.ipynb",
  "Circulate. Most common stall: they paste code without the imports.");

/* ---------------------------------------------------------------- 10 pipeline */
{
  const s = light("The pipeline you're about to build", "This is the whole Python block on one slide.");
  const stages = [
    ["Transcript", "raw text", MUTE],
    ["Word counts", "n_words, TTR", GREEN],
    ["POS tagging", "content vs filler", GREEN],
    ["Semantics", "TF-IDF similarity", GREEN],
    ["Model", "classify group", BERRY],
  ];
  stages.forEach(([t, d, c], i) => {
    const x = 0.55 + i * 2.52;
    card(s, x, 2.5, 2.15, 1.7);
    s.addText(t, { x: x, y: 2.7, w: 2.15, h: 0.4, fontSize: 15, bold: true, color: c, fontFace: H, align: "center", margin: 0 });
    s.addText(d, { x: x, y: 3.15, w: 2.15, h: 0.7, fontSize: 12, color: MUTE, fontFace: M, align: "center", margin: 0 });
    if (i < 4) s.addShape(p.ShapeType.rightArrow, { x: x + 2.22, y: 3.2, w: 0.24, h: 0.28, fill: { color: LINE } });
  });
  s.addText("\"NLP\" is mostly arithmetic on words.", { x: PAD, y: 4.8, w: 11.6, h: 0.5, fontSize: 20, bold: true, color: INK, fontFace: H, margin: 0 });
  s.addText("Counting, dividing, and comparing. The heavy machinery comes out only when the arithmetic runs out. Most published discourse measures are in the first two boxes.",
    { x: PAD, y: 5.35, w: 11.0, h: 0.9, fontSize: 15, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 22 });
}

/* ---------------------------------------------------------------- 11 data */
{
  const s = light("The data (synthetic, and that's the point)", "Point at make_data.py. The honest answer to 'can I use my real data' is: make a synthetic twin of it.");
  s.addTable([
    [{ text: "60 people", options: { bold: true, color: PAPER, fill: { color: INK } } },
     { text: "30 controls  ·  30 with post-stroke aphasia", options: { color: PAPER, fill: { color: INK } } }],
    ["transcript", "What they said describing a kitchen scene"],
    ["wab_aq", "Aphasia severity, 0–100. Higher = less impaired. Controls sit at ~99."],
    ["group, age, sex, education", "The usual"],
    ["transcripts_long.csv", "The 30 patients again at 12 months. 60 rows — but only 30 people."],
  ], { x: PAD, y: 1.8, w: 11.6, colW: [3.4, 8.2], fontSize: 14, fontFace: B,
       border: { pt: 1, color: LINE }, rowH: 0.52, valign: "middle", color: "3A3A44" });

  card(s, PAD, 5.0, 11.6, 1.75, "FBF0F4");
  s.addText("Not one word of this was said by a real person.", { x: PAD + 0.4, y: 5.15, w: 10.8, h: 0.4, fontSize: 17, bold: true, color: BERRY, fontFace: H, margin: 0 });
  s.addText("Every transcript came out of data/make_data.py. Which is exactly why we can paste it into a chatbot for three hours. Remember how this feels — you don't get it back with real data.",
    { x: PAD + 0.4, y: 5.6, w: 10.8, h: 1.0, fontSize: 14, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 20 });
}

/* ---------------------------------------------------------------- 12 TRAP 1 */
{
  const s = light("Trap 1 — the AI will pool your controls", "Python Task 6. Native chart: same measure, two decisions.");
  s.addText("Variance in severity explained by how many words someone produced",
    { x: PAD, y: 1.35, w: 11.6, h: 0.4, fontSize: 15, italic: true, color: MUTE, fontFace: B, margin: 0 });
  s.addChart(p.ChartType.bar, [{
    name: "R² (variance explained)",
    labels: ["All 60 people\n(controls pooled in)", "Aphasia group only\n(the honest number)"],
    values: [0.70, 0.36],
  }], {
    x: PAD, y: 1.85, w: 6.6, h: 4.3, barDir: "col", barGapWidthPct: 90,
    chartColors: [BERRY, GREEN], showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00",
    dataLabelColor: INK, dataLabelFontSize: 15, dataLabelFontBold: true,
    valAxisMaxVal: 0.8, valAxisHidden: true,
    catAxisLabelColor: "3A3A44", catAxisLabelFontSize: 12,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  card(s, PAD + 7.0, 1.85, 4.6, 4.3, WASH);
  s.addText("Why", { x: PAD + 7.3, y: 2.05, w: 4.0, h: 0.4, fontSize: 17, bold: true, color: INK, fontFace: H, margin: 0 });
  s.addText("Controls all score ~99 on the WAB. They have no variance to explain.\n\nPool them in and half your \"explained variance\" is just the fact that patients differ from controls. Which you knew before you started.\n\nThe code runs. Nothing warns you. The number is simply twice as impressive as it deserves to be.",
    { x: PAD + 7.3, y: 2.55, w: 4.0, h: 3.4, fontSize: 13, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 19 });
}

/* ---------------------------------------------------------------- 13 PART 2 */
dark("Part 2 — R", "Statistics, and a figure you'd actually publish\n\n50 minutes  ·  02_r_starter.R",
  "Remind them: Save a Permanent Copy. Say it three times.");

/* ---------------------------------------------------------------- 14 ggplot */
{
  const s = light("This is the best thing an AI does for you", "Be honest and enthusiastic here. This is the genuine, unambiguous win.");
  s.addImage({ path: "outputs/figure1.png", x: PAD, y: 1.6, w: 6.2, h: 4.43 });
  s.addText("Nobody memorises ggplot theme arguments.", { x: PAD + 6.7, y: 1.9, w: 4.9, h: 0.9, fontSize: 21, bold: true, color: INK, fontFace: H, margin: 0, lineSpacing: 28 });
  s.addText("Nobody should. It is pure syntax lookup — high tedium, zero insight, and you'd have spent forty minutes in Stack Overflow for this.\n\nYou describe the figure you want in English. It writes the theme() call. You look at it, you don't like the legend, you say so, it fixes it.\n\nThat loop is the whole job, and it is genuinely, permanently better than what came before.",
    { x: PAD + 6.7, y: 3.0, w: 4.9, h: 3.2, fontSize: 14, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 21 });
}

/* ---------------------------------------------------------------- 15 TRAP 2 */
{
  const s = light("Trap 2 — the finding that quietly evaporated", "R Task 4. Nothing errored. That's the whole horror of it.");
  card(s, PAD, 1.75, 5.5, 2.2, "F1F7F3");
  s.addText("On its own", { x: PAD + 0.35, y: 1.95, w: 4.8, h: 0.35, fontSize: 14, bold: true, color: GREEN, fontFace: B, margin: 0 });
  s.addText("lm(wab_aq ~ content_word_ratio)", { x: PAD + 0.35, y: 2.35, w: 5.0, h: 0.35, fontSize: 13, color: "3A3A44", fontFace: M, margin: 0 });
  s.addText("p = .004", { x: PAD + 0.35, y: 2.8, w: 4.8, h: 0.9, fontSize: 40, bold: true, color: GREEN, fontFace: H, margin: 0 });

  card(s, PAD + 6.1, 1.75, 5.5, 2.2, "FBF0F4");
  s.addText("With n_words in the model", { x: PAD + 6.45, y: 1.95, w: 4.8, h: 0.35, fontSize: 14, bold: true, color: BERRY, fontFace: B, margin: 0 });
  s.addText("+ type_token_ratio + n_words + age", { x: PAD + 6.45, y: 2.35, w: 5.0, h: 0.35, fontSize: 13, color: "3A3A44", fontFace: M, margin: 0 });
  s.addText("p = .055", { x: PAD + 6.45, y: 2.8, w: 4.8, h: 0.9, fontSize: 40, bold: true, color: BERRY, fontFace: H, margin: 0 });

  s.addText("Same data. Same variable. Same afternoon.", { x: PAD, y: 4.3, w: 11.6, h: 0.5, fontSize: 20, bold: true, color: INK, fontFace: H, margin: 0 });
  s.addText("n_words quietly ate its variance — people who say more say more content words. Both models ran perfectly. Neither printed a warning. Your headline finding became a footnote and the only thing standing between you and reporting the first number is that you happened to look.",
    { x: PAD, y: 4.9, w: 11.6, h: 1.3, fontSize: 15, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 23 });
  s.addText("Ask it: \"what is this model assuming about my predictors?\" It gives a good answer. It just never volunteers one.",
    { x: PAD, y: 6.25, w: 11.6, h: 0.5, fontSize: 14, bold: true, italic: true, color: BERRY, fontFace: B, margin: 0 });
}

/* ---------------------------------------------------------------- 16 TRAP 3 */
{
  const s = light("Trap 3 — the wrong model HID a real effect", "R Task 6. This is the one that surprises people. They expect false positives.");
  s.addText("30 patients, measured twice. 60 rows — but 30 people.",
    { x: PAD, y: 1.3, w: 11.6, h: 0.4, fontSize: 15, italic: true, color: MUTE, fontFace: B, margin: 0 });

  card(s, PAD, 1.85, 5.5, 2.6, "FBF0F4");
  s.addText("The naive model", { x: PAD + 0.35, y: 2.05, w: 4.8, h: 0.35, fontSize: 14, bold: true, color: BERRY, fontFace: B, margin: 0 });
  s.addText("lm(wab_aq ~ timepoint)", { x: PAD + 0.35, y: 2.45, w: 5.0, h: 0.35, fontSize: 13, color: "3A3A44", fontFace: M, margin: 0 });
  s.addText("p = .056", { x: PAD + 0.35, y: 2.9, w: 4.8, h: 0.8, fontSize: 36, bold: true, color: BERRY, fontFace: H, margin: 0 });
  s.addText("\"No significant improvement.\"", { x: PAD + 0.35, y: 3.75, w: 4.8, h: 0.4, fontSize: 14, italic: true, color: BERRY, fontFace: B, margin: 0 });

  card(s, PAD + 6.1, 1.85, 5.5, 2.6, "F1F7F3");
  s.addText("The correct model", { x: PAD + 6.45, y: 2.05, w: 4.8, h: 0.35, fontSize: 14, bold: true, color: GREEN, fontFace: B, margin: 0 });
  s.addText("lmer(wab_aq ~ timepoint + (1|id))", { x: PAD + 6.45, y: 2.45, w: 5.0, h: 0.35, fontSize: 13, color: "3A3A44", fontFace: M, margin: 0 });
  s.addText("t = 5.2", { x: PAD + 6.45, y: 2.9, w: 4.8, h: 0.8, fontSize: 36, bold: true, color: GREEN, fontFace: H, margin: 0 });
  s.addText("+7.1 WAB points. Clear recovery.", { x: PAD + 6.45, y: 3.75, w: 4.8, h: 0.4, fontSize: 14, italic: true, color: GREEN, fontFace: B, margin: 0 });

  s.addText("The wrong model didn't invent an effect. It hid one.",
    { x: PAD, y: 4.85, w: 11.6, h: 0.6, fontSize: 24, bold: true, color: INK, fontFace: H, margin: 0 });
  s.addText("Throwing away the pairing threw away the power to see a real recovery. You'd have written \"no significant improvement\" in a grant, and you'd have been wrong — and the code would have run beautifully the entire time.",
    { x: PAD, y: 5.5, w: 11.6, h: 1.1, fontSize: 15, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 23 });
}

/* ---------------------------------------------------------------- 17 factcheck */
{
  const s = light("The fact-check", "DO THIS TOGETHER ON THE PROJECTOR. It is the punchline of the day.");
  card(s, PAD, 1.7, 11.6, 1.15, INK);
  s.addText("\"Write the Results paragraph for my model in APA style.\"",
    { x: PAD + 0.4, y: 1.7, w: 10.8, h: 1.15, fontSize: 19, color: PAPER, fontFace: M, valign: "middle", margin: 0 });

  s.addText("Now check every number against tidy(m1), glance(m1), nobs(m1). Line by line. Out loud.",
    { x: PAD, y: 3.1, w: 11.6, h: 0.45, fontSize: 16, bold: true, color: INK, fontFace: B, margin: 0 });

  const errs = [
    "A degrees-of-freedom value that appears nowhere in your output",
    "A predictor called \"significant\" at p = .055",
    "A coefficient reported with the sign flipped",
    "An R² or an F statistic it never actually saw",
  ];
  errs.forEach((e, i) => {
    const y = 3.75 + i * 0.6;
    s.addShape(p.ShapeType.ellipse, { x: PAD + 0.05, y: y + 0.09, w: 0.2, h: 0.2, fill: { color: BERRY } });
    s.addText(e, { x: PAD + 0.45, y: y, w: 11.0, h: 0.4, fontSize: 15, color: "3A3A44", fontFace: B, margin: 0 });
  });

  s.addText("It will write a better paragraph than you would have. And it will lie in it. Both of those are true, and you have to hold both.",
    { x: PAD, y: 6.25, w: 11.6, h: 0.6, fontSize: 15, bold: true, italic: true, color: BERRY, fontFace: B, margin: 0, lineSpacing: 22 });
}

/* ---------------------------------------------------------------- 18 five errors */
{
  const s = light("The five it gets wrong, in order of frequency", "This slide is in PROMPTS.md too. Tell them that.");
  const rows = [
    ["Hallucinated functions", "Confidently calls tidystats::auto_model(). No such thing exists.", "\"Is this package real? Show me the docs.\""],
    ["Wrong test for your design", "It does not know you have repeated measures. Unless you tell it.", "\"What is this test assuming about my design?\""],
    ["Silent scope errors", "Models everyone when you meant a subgroup. Drops NAs without a word.", "\"Print nrow() before and after every filter.\""],
    ["Invented numbers in prose", "Beautiful APA paragraphs containing an F it never computed.", "\"Check every number against the model object.\""],
    ["Plausible-but-wrong stats", "p = .07 described as significant. A sign flipped, reported with total serenity.", "\"Read the output yourself. Every time.\""],
  ];
  rows.forEach(([t, d, fix], i) => {
    const y = 1.6 + i * 1.03;
    card(s, PAD, y, 11.6, 0.92, i % 2 ? WASH : PAPER);
    numDot(s, PAD + 0.2, y + 0.25, i + 1, [BERRY, BERRY, AMBER, AMBER, GREEN][i]);
    s.addText(t, { x: PAD + 0.82, y: y + 0.06, w: 3.0, h: 0.4, fontSize: 14, bold: true, color: INK, fontFace: B, margin: 0 });
    s.addText(d, { x: PAD + 0.82, y: y + 0.44, w: 5.2, h: 0.42, fontSize: 12, color: MUTE, fontFace: B, margin: 0 });
    s.addText(fix, { x: PAD + 6.3, y: y, w: 5.1, h: 0.92, fontSize: 12, color: "3A3A44", fontFace: M, valign: "middle", margin: 0 });
  });
}

/* ---------------------------------------------------------------- 19 rules */
{
  const s = light("The rules that don't bend", "Slow down here. This is the part their compliance office cares about.");
  const rules = [
    [BERRY, "Never paste real patient data into a chatbot.", "Not transcripts. Not MRNs. Not \"de-identified\" text you haven't personally checked. Share the SCHEMA, not the rows — column names and a fabricated example row are enough to get working code."],
    [AMBER, "Run it. Read it. Then trust it. In that order.", "Code that runs without error can still be answering a different question than the one you asked."],
    [GREEN, "If you can't explain it, you can't publish it.", "Not a moral point — a practical one. You are the person defending it in review, and in your own head at 2am."],
  ];
  rules.forEach(([c, t, d], i) => {
    const y = 1.7 + i * 1.65;
    card(s, PAD, y, 11.6, 1.45);
    s.addShape(p.ShapeType.ellipse, { x: PAD + 0.3, y: y + 0.5, w: 0.42, h: 0.42, fill: { color: c } });
    s.addText(t, { x: PAD + 1.0, y: y + 0.14, w: 10.3, h: 0.42, fontSize: 17, bold: true, color: INK, fontFace: H, margin: 0 });
    s.addText(d, { x: PAD + 1.0, y: y + 0.58, w: 10.3, h: 0.8, fontSize: 13, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 19 });
  });
  s.addText("And say what you did. Journals increasingly require it. One sentence in the methods. Keep the chat log.",
    { x: PAD, y: 6.7, w: 11.6, h: 0.4, fontSize: 14, italic: true, color: MUTE, fontFace: B, margin: 0 });
}

/* ---------------------------------------------------------------- 20 next */
{
  const s = light("Where this goes next", "Show, don't teach. Demo `claude` in a terminal for 90 seconds.");
  const tiers = [
    [MUTE, "Today", "Chat in one tab, code in another. Copy, paste, run, check.", "Works everywhere. Free. Start here."],
    [GREEN, "In-IDE", "The assistant lives inside the editor. Colab's Gemini panel. Copilot in RStudio.", "Same skill. Less copy-pasting."],
    [BERRY, "Agentic", "Claude Code in a terminal: \"read the CSV, compute the measures, fit the model, make the figure.\" It just does it.", "Ninety seconds for today's ninety minutes."],
  ];
  tiers.forEach(([c, t, d, note], i) => {
    const x = PAD + i * 4.0;
    card(s, x, 1.8, 3.6, 3.5);
    s.addShape(p.ShapeType.ellipse, { x: x + 0.3, y: 2.1, w: 0.45, h: 0.45, fill: { color: c } });
    s.addText(t, { x: x + 0.3, y: 2.7, w: 3.0, h: 0.42, fontSize: 18, bold: true, color: INK, fontFace: H, margin: 0 });
    s.addText(d, { x: x + 0.3, y: 3.2, w: 3.0, h: 1.4, fontSize: 13, color: "3A3A44", fontFace: B, margin: 0, lineSpacing: 18 });
    s.addText(note, { x: x + 0.3, y: 4.7, w: 3.0, h: 0.5, fontSize: 12, italic: true, color: c, fontFace: B, margin: 0 });
  });
  s.addText("The agent will do it faster than you did. The thing that changed today is that you can now read what it did and tell whether it's right. That is the entire difference between a tool and a liability.",
    { x: PAD, y: 5.6, w: 11.6, h: 1.2, fontSize: 16, bold: true, color: INK, fontFace: B, margin: 0, lineSpacing: 24 });
}

/* ---------------------------------------------------------------- 21 close */
dark("You are now the senior author\non everything it writes for you.",
  "Act like it.\n\nKeep PROMPTS.md. That's the artifact.",
  "Final line. Land it and stop talking.");

p.writeFile({ fileName: "slides/coding_with_ai.pptx" }).then(() => console.log("deck written"));
