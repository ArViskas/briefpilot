const activityList = document.querySelector("#activityList");
const runButton = document.querySelector("#runButton");
const actionPanel = document.querySelector("#actionPanel");
const statusBadge = document.querySelector("#statusBadge");
const timelineValue = document.querySelector("#timelineValue");
const websiteValue = document.querySelector("#websiteValue");

const initialActivity = [
  ["✓", "Inquiry received"],
  ["✓", "Requirements extracted: WooCommerce · redesign · discount visibility"],
  ["!", "3 missing details found before qualification"]
];

const renderActivity = (items) => {
  activityList.innerHTML = "";
  items.forEach(([icon, text, wait = false]) => {
    const item = document.createElement("li");
    item.innerHTML = `<span class="activity-icon ${wait ? "wait" : ""}">${icon}</span><span>${text}</span>`;
    activityList.appendChild(item);
  });
};

renderActivity(initialActivity);

let step = 0;

runButton.addEventListener("click", () => {
  if (step === 0) {
    renderActivity([
      ...initialActivity,
      ["✓", "Clarification prepared"],
      ["→", "Waiting for client reply", true]
    ]);

    actionPanel.innerHTML = `
      <div>
        <p class="eyebrow">Clarification ready</p>
        <h3>Only ask what is needed.</h3>
        <ul>
          <li>Could you share the current store URL?</li>
          <li>Is there a target launch date or preferred timeline?</li>
          <li>Should this cover only the homepage, or also product and cart/checkout discount presentation?</li>
        </ul>
      </div>
      <button id="clientReplyButton" class="primary-button" type="button">Simulate client reply</button>
    `;

    document.querySelector("#clientReplyButton").addEventListener("click", showHumanDecision);
    step = 1;
  }
});

function showHumanDecision() {
  websiteValue.textContent = "example-shop.test";
  timelineValue.textContent = "3 weeks";

  renderActivity([
    ["✓", "Inquiry received"],
    ["✓", "Requirements extracted"],
    ["✓", "Clarification sent"],
    ["✓", "Client reply received"],
    ["✓", "Opportunity updated"],
    ["!", "Commercial judgment required", true]
  ]);

  statusBadge.className = "status ready";
  statusBadge.textContent = "Human decision required";

  actionPanel.innerHTML = `
    <div>
      <p class="eyebrow">Human decision required</p>
      <h3>Qualified opportunity — ready for review.</h3>
      <div class="decision-grid">
        <div><span>Scope signal</span><strong>Homepage + product/cart discount UX</strong></div>
        <div><span>Main risk</span><strong>Existing custom checkout logic</strong></div>
        <div><span>Recommended next action</span><strong>Technical review before commitment</strong></div>
        <div><span>Human owns</span><strong>Scope · price · deadline · final reply</strong></div>
      </div>
    </div>
    <button class="primary-button" type="button">Open draft reply</button>
  `;
}
