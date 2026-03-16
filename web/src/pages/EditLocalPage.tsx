import { useParams, useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/common/PageHeader";
import { LocalForm } from "@/components/locais/LocalForm";
import { LocalMachinesSection } from "@/components/locais/LocalMachinesSection";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { 
  useLocalDetail, 
  useUpdateLocal, 
  useCreateMaquina, 
  useUpdateMaquina, 
  useDeleteMaquina 
} from "@/hooks/useLocal";
import type { LocalCreate, LocalUpdate, MaquinaCreate, MaquinaUpdate } from "@/types/local";

export const EditLocalPage = () => {
  const { localId } = useParams<{ localId: string }>();
  const navigate = useNavigate();
  
  const { data, isLoading, isError, error } = useLocalDetail(localId);
  const updateLocalMut = useUpdateLocal();
  const createMaquinaMut = useCreateMaquina();
  const updateMaquinaMut = useUpdateMaquina();
  const deleteMaquinaMut = useDeleteMaquina();

  if (isLoading) {
    return (
      <AppShell title="K">
        <LoadingState message="Buscando detalhes do local..." />
      </AppShell>
    );
  }

  if (isError || !data?.local) {
    return (
      <AppShell title="K">
        <ErrorState error={error as Error || new Error("Local não encontrado.")} />
        <div className="text-center">
          <button onClick={() => navigate("/inventory")} className="text-indigo-600 underline">
            Voltar ao Inventário
          </button>
        </div>
      </AppShell>
    );
  }

  const { local, maquinas } = data;

  const handleUpdateLocal = async (formData: LocalCreate | LocalUpdate) => {
    try {
      await updateLocalMut.mutateAsync({ local_id: local.local_id, data: formData as LocalUpdate });
      alert("Local atualizado com sucesso.");
    } catch (e: unknown) {
      if (e instanceof Error) alert(`Erro ao atualizar: ${e.message}`);
    }
  };

  const handleCreateMaquina = async (formData: MaquinaCreate) => {
    try {
      await createMaquinaMut.mutateAsync({ local_id: local.local_id, data: formData });
    } catch (e: unknown) {
      if (e instanceof Error) alert(`Erro ao adicionar máquina: ${e.message}`);
    }
  };

  const handleUpdateMaquina = async (maquina_id: number, formData: MaquinaUpdate) => {
    try {
      await updateMaquinaMut.mutateAsync({ local_id: local.local_id, maquina_id, data: formData });
    } catch (e: unknown) {
      if (e instanceof Error) alert(`Erro ao atualizar máquina: ${e.message}`);
    }
  };

  const handleDeleteMaquina = async (maquina_id: number) => {
    try {
      await deleteMaquinaMut.mutateAsync({ local_id: local.local_id, maquina_id });
    } catch (e: unknown) {
      if (e instanceof Error) alert(`Erro ao deletar máquina: ${e.message}`);
    }
  };

  return (
    <AppShell title={`Editar: ${local.local_id}`}>
      <div className="max-w-4xl mx-auto space-y-6 pb-12">
        <PageHeader 
          title={`Editar Local: ${local.local_id}`} 
          description="Altere as propriedades do local e gerencie o hardware que pertence a ele." 
        />
        
        <LocalMachinesSection 
          localId={local.local_id}
          maquinas={maquinas}
          onCreate={handleCreateMaquina}
          onUpdate={handleUpdateMaquina}
          onDelete={handleDeleteMaquina}
          isPendingCreate={createMaquinaMut.isPending}
        />

        <LocalForm 
          initialData={local}
          onSubmit={handleUpdateLocal} 
          isLoading={updateLocalMut.isPending} 
        />
      </div>
    </AppShell>
  );
};
