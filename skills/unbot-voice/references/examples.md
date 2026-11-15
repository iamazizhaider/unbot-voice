# Before / after examples

Each example shows an AI draft, the facts the user supplied when asked, and the rewrite. The scanner scores (`scripts/scan.py`, tells per 1,000 words) are included for reference. The specifics in each rewrite come from the "user supplied" line. Humanizing never makes them up. If the user can't supply a fact, the claim gets cut or marked as a gap (see example 4).

---

## 1. LinkedIn post (score 194 → 0)

**Before**
> I almost didn't post this.
>
> But here's the thing: after 10 years in marketing, I've learned that success isn't about working harder — it's about working smarter.
>
> Last quarter, our team faced a pivotal moment. [...] The result? A 40% increase in qualified leads.
>
> No fancy tools. No massive budget. Just a relentless focus on our customers.
>
> - 🚀 **Listen first:** Your customers will tell you what they need. [...]
>
> Growth isn't a destination — it's a journey. And honestly? I'm just getting started.

**User supplied:** leads had been flat for three quarters; they paused paid ads for six weeks and called ~30 customers; customers kept asking about CRM compatibility; they rewrote three landing pages.

**After**
> Last quarter our lead numbers were flat for the third quarter running, so we stopped running paid campaigns for six weeks and called customers instead. About 30 of them.
>
> Most said the same thing: our landing pages explained features they didn't care about and skipped the one question they all had, which was whether it worked with their existing CRM. We rewrote three pages around that answer.
>
> Qualified leads went up 40% the following quarter. Same budget, same tools.
>
> I don't think there's a big lesson here beyond the obvious one. We'd been guessing what people wanted when we could have asked.

**What changed:** the "here's the thing / the result? / and honestly?" drama is gone, and so are the "not X, it's Y" lines, the "No X. No Y. Just Z." beat, the emoji bullets and the journey metaphor. The post is now the story itself, and the ending refuses to make a big lesson out of it.

---

## 2. Cold email (score 212 → 0)

**Before**
> Subject: Unlocking New Opportunities for [Company]
>
> I hope this email finds you well! I came across your company and was truly impressed by your innovative approach to sustainable packaging. [...] we specialize in helping forward-thinking companies like yours streamline their supply chain operations, enhance efficiency, and drive sustainable growth. Our robust platform seamlessly integrates [...] I'd love to explore how we can support your journey.

**User supplied:** the recipient (Dana) posted about switching to compostable mailers; the sender's product routes return labels by material; a client, Kindred Goods, now gets ~70% of mailers to compost.

**After**
> Subject: Your returns are going to the wrong warehouse
>
> Hi Dana,
>
> I saw your post about switching to compostable mailers. One thing that tends to come up for brands that make that switch is that returned packaging ends up in general waste, because the carrier's return labels still route to your main warehouse instead of a compost partner.
>
> We fixed that for Kindred Goods last spring. Their return labels now route by material, and about 70% of mailers come back to a composting facility.
>
> If that's a problem you're running into, I can show you how their setup works in 15 minutes. If not, no worries.
>
> Sam

**What changed:** the placeholders are filled in, and the boilerplate opener and the list of three benefits are cut. It names one specific problem with one specific result. The subject line says something.

---

## 3. Encyclopedia-style paragraph (score 277 → 5)

**Before**
> Millbrook is a small town nestled in the heart of the Hudson Valley, renowned for its rich history and vibrant arts scene. Founded in 1823, the town has played a significant role in the region's agricultural development, leaving an indelible mark on the local landscape. [...] The annual Harvest Festival draws thousands of visitors each year, highlighting the town's enduring agricultural traditions.
>
> Despite its charm, Millbrook faces challenges [...] Despite these challenges, local leaders remain optimistic [...]

**User supplied (from sources):** Dutchess County; dairy center through the late 1800s; 2020 census 1,452 (1990: 1,810); museum in the old Thorne schoolhouse; festival every October since 1952, ~6,000 attendees in 2023 per county tourism office.

**After**
> Millbrook is a town in Dutchess County, New York, in the Hudson Valley. It was founded in 1823 and was a dairy-farming center through the late 19th century. The population was 1,452 at the 2020 census, down from 1,810 in 1990.
>
> The Millbrook Historical Society runs a museum in the former Thorne schoolhouse. The town has held a harvest festival each October since 1952; the county tourism office estimated attendance at 6,000 in 2023.

**What changed:** the brochure words (nestled, renowned, vibrant, rich) are gone, along with "played a significant role", "indelible mark", the "-ing" tail and the "despite these challenges" paragraph. The decline is now just a census number, and the reader can draw their own conclusion. The scanner's remaining point is for uniform sentence rhythm, which is normal for this genre, so it was left alone.

---

## 4. Bio with missing facts (asking instead of inventing)

**Before**
> Sarah Chen is a visionary leader and passionate advocate for diversity in tech. With over 15 years of experience in software engineering, she has played a pivotal role in shaping the conversation around inclusive design. Her work serves as a testament to the power of combining technical excellence with empathy. [...] She currently serves as VP of Engineering at Lumen, where she leads a diverse team of 200 engineers, fostering a culture of collaboration, creativity, and continuous learning.

**User supplied:** only the job title and team size.

**After (first pass, with gaps marked)**
> Sarah Chen is VP of Engineering at Lumen, where she runs a team of about 200 engineers. Before that she [previous role: where, and one concrete thing she built or changed].
>
> [Press: which outlet, and what about? Keep only if it's about her work.]
>
> Outside work she [one specific hobby detail, or cut this line].

**Note to user:** "I cut 'visionary leader', 'pivotal role in shaping the conversation' and 'testament to' because there's no concrete fact behind them yet. Give me one project she led and I'll write the line."

---

## 5. Argumentative essay paragraph (score 197 → 0)

**Before**
> Social media has fundamentally transformed the way we communicate, connect, and consume information. While it offers unprecedented opportunities for global connection, it also presents significant challenges that warrant careful consideration. On one hand, [...] On the other hand, experts argue [...] Furthermore, [...] Moreover, [...] In conclusion, social media is a double-edged sword. It is important to note that the key lies in finding a balance [...]

**User supplied:** the writer's actual position (ranking algorithms are the problem, not publishing), and the example of the leaked 2021 Facebook research.

**After**
> Social media made it cheap for anyone to publish to a large audience. That changed who gets heard. A teenager with a phone can now document a police stop and reach more people than the local paper does.
>
> The same cheapness is the problem. When publishing costs nothing, the platforms decide what gets seen, and they pick whatever keeps people scrolling. Outrage does that well. A 2021 internal Facebook study, later leaked, found the company's ranking changes in 2018 had made angry posts spread further.
>
> So I don't think the question is whether social media is good or bad. It's who should control the ranking, and so far the answer has been a handful of companies that profit from the worst of it.

**What changed:** the both-sides seesaw is replaced by a thesis. "Experts argue" became a named source. The stacked transitions, "in conclusion" and "double-edged sword" are gone, and sentence length now varies (6 to 30 words).

---

## 6. Status update (score 184 → 0)

**Before**
> I wanted to provide a quick update on the Q3 platform migration. Overall, the project is progressing steadily and remains aligned with our strategic priorities.
>
> - **Database migration:** Successfully completed, ensuring seamless data continuity.
> - **API updates:** On track, with robust testing underway.
> - **Frontend redesign:** Slightly delayed due to unforeseen dependencies.
>
> It's worth noting that the frontend delay does not impact our overall timeline. The team has demonstrated remarkable resilience [...] Let me know if you have any questions or would like me to provide additional details!

**User supplied:** DB finished Tuesday, no missing records; API ships the 14th; frontend is a week late because of an auth library change; launch is Oct 30; Priya is the other contact.

**After**
> Hi team,
>
> Q3 migration update. The database move finished on Tuesday and we haven't found any missing records. API changes are in testing and should ship on the 14th as planned.
>
> The frontend redesign is about a week behind because the auth library we depend on changed its session handling. That week was already in our buffer, so the October 30 launch date doesn't move.
>
> Questions to me or Priya.

**What changed:** dates replace "progressing steadily", and the real cause replaces "unforeseen dependencies". The bold-label bullets are now two short paragraphs. The praise filler and the chatbot closer are cut.
