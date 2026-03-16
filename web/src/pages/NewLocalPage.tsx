import { useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/common/PageHeader";
import { LocalForm } from "@/components/locais/LocalForm";
import { useCreateLocal } from "@/hooks/useLocal";
import type { LocalCreate, LocalUpdate } from "@/types/local";

export const NewLocalPage = () => {
  const navigate = useNavigate();
  const createMutation = useCreateLocal();

  const handleCreated = async (data: LocalCreate | LocalUpdate) => {
    try {
      const resp = await createMutation.mutateAsync(data as LocalCreate);
      alert(`Local criado com sucesso: ${resp.local_id}`);
      navigate(`/locais/${resp.local_id}/editar`);
    } catch (e: unknown) {
      if (e instanceof Error) {
        alert(`Erro ao criar local: ${e.message}`);
      } else {
        alert("Erro desconhecido ao criar local.");
      }
    }
  };

  return (
    <AppShell title="Novo Local">
      <div className="max-w-4xl mx-auto space-y-6 pb-12">
        <PageHeader 
          title="Cadastrar Novo Local" 
          description="Adicione uma nova sala ou laboratório ao inventário. As máquinas podem ser adicionadas na próxima etapa." 
        />
        
        <LocalForm 
          onSubmit={handleCreated} 
          isLoading={createMutation.isPending} 
        />
      </div>
    </AppShell>
  );
};
