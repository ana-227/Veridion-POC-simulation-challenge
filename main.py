import pandas as pd

def run_cleanup(input_file, output_file):
    # Incarcarea datelor
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: File not found.")
        return

    # 1. ENTITY RESOLUTION
    # Crearea unei coloane noi pentru decizia luata (care dintre cele 5 companii trebuia luata in considerare)
    df['is_best_match'] = False

    # Identificare cheilor unice de intrare
    unique_keys = df['input_row_key'].unique()

    for key in unique_keys:
        # Luarea tuturor candidatilor pentru acest furnizor
        candidates = df[df['input_row_key'] == key]

        # Marcarea primului candidat ca fiind cel mai bun ("Best Match")
        first_candidate_idx = candidates.index[0]
        df.at[first_candidate_idx, 'is_best_match'] = True

    # 2. DATA ANALYSIS AND QC
    # Filtrarea companiilor pe care le-am ales ca fiind "Best Match"
    selected_companies = df[df['is_best_match'] == True].copy()

    # Verificarea datelor lipsa pentru venituri (Revenue), fiind necesara pentru strategia de cost-saving
    missing_revenue = selected_companies['revenue'].isna().sum()
    total_selected = len(selected_companies)

    # Verificarea existentei erorilor de tip #ERROR!
    error_mask = df.apply(lambda row: row.astype(str).str.contains('#ERROR!').any(), axis=1)
    rows_with_errors = error_mask.sum()

    # 3. RAPORTARE REZULTATE
    print(f"Total input records processed: {len(unique_keys)}")
    print(f"Successful matches identified: {total_selected}")
    print(f"QC: {missing_revenue} records are missing revenue data")
    print(f"QC: {rows_with_errors} rows contain data corruption strings (#ERROR!)")

    # 4. SALVARE REZULTATE
    # Eliminarea coloanelor fara nume sau goale daca exista
    cols_to_keep = [c for c in df.columns if not c.startswith('Unnamed')]
    df[cols_to_keep].to_csv(output_file, index=False)

if __name__ == '__main__':
    INPUT = 'presales_data_sample.csv'
    OUTPUT = 'resolved_presales_data_sample.csv'

    run_cleanup(INPUT, OUTPUT)