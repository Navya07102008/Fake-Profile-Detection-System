const SAMPLE_PERSONAS = {
  spambot: {
    username: "bot_spammer_9921",
    followers: 12,
    following: 2850,
    posts: 0,
    age: 7,
    bio: "",
    likes: 0,
    comments: 0,
    has_pic: false,
    verified: false,
    external_url: false
  },
  influencer: {
    username: "dr_elena_ai_official",
    followers: 94500,
    following: 820,
    posts: 1280,
    age: 2400,
    bio: "AI Research Scientist | Keynote Speaker | Author of Deep Cyber Systems. Contact: press@elena-ai.org",
    likes: 3420,
    comments: 410,
    has_pic: true,
    verified: true,
    external_url: true
  },
  ghost: {
    username: "ghost_lurker_404",
    followers: 18,
    following: 340,
    posts: 0,
    age: 520,
    bio: "",
    likes: 0,
    comments: 0,
    has_pic: false,
    verified: false,
    external_url: false
  },
  organic: {
    username: "cyber_tech_sarah",
    followers: 4820,
    following: 620,
    posts: 345,
    age: 1240,
    bio: "Full-stack cloud dev. Coffee enthusiast and open-source contributor.",
    likes: 145.5,
    comments: 18.2,
    has_pic: true,
    verified: false,
    external_url: true
  },
  bought_followers: {
    username: "bought_followers_scam",
    followers: 45000,
    following: 120,
    posts: 8,
    age: 45,
    bio: "DM for promotions and collabs 🚀",
    likes: 3.5,
    comments: 0.2,
    has_pic: true,
    verified: false,
    external_url: false
  }
};

function loadPersona(type) {
  const p = SAMPLE_PERSONAS[type];
  if (!p) return;

  const uInput = document.getElementById("id_username");
  const fCount = document.getElementById("id_followers_count");
  const folCount = document.getElementById("id_following_count");
  const pCount = document.getElementById("id_posts_count");
  const ageCount = document.getElementById("id_account_age_days");
  const bioInput = document.getElementById("id_bio_text");
  const likesInput = document.getElementById("id_avg_likes");
  const commInput = document.getElementById("id_avg_comments");
  const picCheck = document.getElementById("id_has_profile_pic");
  const verCheck = document.getElementById("id_is_verified");
  const urlCheck = document.getElementById("id_has_external_url");

  if (uInput) uInput.value = p.username;
  if (fCount) fCount.value = p.followers;
  if (folCount) folCount.value = p.following;
  if (pCount) pCount.value = p.posts;
  if (ageCount) ageCount.value = p.age;
  if (bioInput) bioInput.value = p.bio;
  if (likesInput) likesInput.value = p.likes;
  if (commInput) commInput.value = p.comments;
  if (picCheck) picCheck.checked = p.has_pic;
  if (verCheck) verCheck.checked = p.verified;
  if (urlCheck) urlCheck.checked = p.external_url;

  updateLivePreview();
}

function updateLivePreview() {
  const followers = parseFloat(document.getElementById("id_followers_count")?.value || 0);
  const following = parseFloat(document.getElementById("id_following_count")?.value || 0);
  const posts = parseFloat(document.getElementById("id_posts_count")?.value || 0);
  const age = parseFloat(document.getElementById("id_account_age_days")?.value || 1);
  const likes = parseFloat(document.getElementById("id_avg_likes")?.value || 0);
  const comments = parseFloat(document.getElementById("id_avg_comments")?.value || 0);

  const ratio = followers / (following + 1);
  const engagement = ((likes + comments) / (followers + 1)) * 100;
  const postDaily = posts / (age + 1);

  const ratioEl = document.getElementById("preview-ratio");
  const engEl = document.getElementById("preview-engagement");
  const postEl = document.getElementById("preview-postdaily");

  if (ratioEl) ratioEl.innerText = ratio.toFixed(3);
  if (engEl) engEl.innerText = engagement.toFixed(2) + "%";
  if (postEl) postEl.innerText = postDaily.toFixed(3);
}

document.addEventListener("DOMContentLoaded", () => {
  const inputs = document.querySelectorAll("#analysisForm input, #analysisForm textarea");
  inputs.forEach(input => {
    input.addEventListener("input", updateLivePreview);
    input.addEventListener("change", updateLivePreview);
  });
  updateLivePreview();
});
