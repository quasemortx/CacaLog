export function formatDate(dateString: string | undefined | null): string {
  if (!dateString || dateString.trim() === "") return "—";

  // Attempt to parse standard ISO strings or common formats.
  // The backend might send 'DD/MM/YYYY HH:mm' or similar.
  // If parsing fails or results in invalid date, return the raw string.
  
  if (dateString.includes("/")) {
      const parts = dateString.split(" ");
      if (parts.length >= 1) {
          const datePart = parts[0];
          const dateParts = datePart.split("/");
          if (dateParts.length === 3) {
             const day = parseInt(dateParts[0], 10);
             const month = parseInt(dateParts[1], 10) - 1;
             const year = parseInt(dateParts[2], 10);
             
             let hours = 0, minutes = 0;
             if (parts.length > 1) {
                 const timePart = parts[1];
                 const timeParts = timePart.split(":");
                 if (timeParts.length >= 2) {
                     hours = parseInt(timeParts[0], 10);
                     minutes = parseInt(timeParts[1], 10);
                 }
             }
             
             const parsedDate = new Date(year, month, day, hours, minutes);
             if (!isNaN(parsedDate.getTime())) {
                return new Intl.DateTimeFormat('pt-BR', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                }).format(parsedDate);
             }
          }
      }
      return dateString;
  }

  const date = new Date(dateString);
  if (isNaN(date.getTime())) {
    return dateString; // Fallback to raw string
  }

  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}

export function normalizeStatus(status: string | undefined | null): string {
    if (!status) return "NAO_AVALIADO";
    return status.toUpperCase().trim().replace(/\s+/g, '_');
}

export function normalizeSector(sector: string | undefined | null): string {
    if (!sector || sector.trim() === "") return "INDEFINIDO";
    return sector.toUpperCase().trim();
}
