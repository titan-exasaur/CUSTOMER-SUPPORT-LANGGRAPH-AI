const API_BASE_URL = "https://8qse6mcm2j.execute-api.us-east-1.amazonaws.com";

const form = document.getElementById("ticketForm");
const ticketText = document.getElementById("ticketText");
const chatWindow = document.getElementById("chatWindow");
const submitBtn = document.getElementById("submitBtn");

function addMessage(type, html) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerHTML = html;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function pollTicket(ticketId) {
  for (let i = 0; i < 12; i++) {
    const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}`);
    const ticket = await response.json();

    if (ticket.status === "resolved" || ticket.status === "escalated" || ticket.status === "failed") {
      addMessage("bot", `
        <div class="result-card">
          <p><strong>Ticket ID:</strong> ${ticket.ticket_id}</p>
          <p><strong>Status:</strong> ${ticket.status}</p>
          <p><strong>Category:</strong> ${ticket.ticket_category || "pending"}</p>
          <p><strong>Urgency:</strong> ${ticket.urgency_level || "pending"}</p>
          <p><strong>Escalation:</strong> ${ticket.needs_escalation ? "Yes" : "No"}</p>
          <p><strong>Response:</strong> ${ticket.draft_response || "No response yet."}</p>
        </div>
      `);
      return;
    }

    await sleep(2500);
  }

  addMessage("system", "<p>Ticket is still processing. Please check again shortly.</p>");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const text = ticketText.value.trim();
  if (!text) return;

  addMessage("user", `<p>${text}</p>`);

  ticketText.value = "";
  submitBtn.disabled = true;
  submitBtn.textContent = "Submitting...";

  try {
    const response = await fetch(`${API_BASE_URL}/tickets`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: "frontend_user",
        ticket_text: text
      })
    });

    const data = await response.json();

    addMessage("system", `<p>Ticket created: <strong>${data.ticket_id}</strong>. Processing now...</p>`);

    await pollTicket(data.ticket_id);
  } catch (error) {
    addMessage("system", "<p>Something went wrong. Please try again.</p>");
    console.error(error);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Submit Ticket";
  }
});