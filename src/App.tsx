import React, { useState, useRef, useEffect } from 'react';
import { 
  Upload, Download, Undo2, RotateCcw, AlertTriangle, Moon, Sun, 
  SplitSquareHorizontal, Image as ImageIcon, BarChart, SlidersHorizontal, Move, Palette, Wand2, RefreshCw, Layers, Globe, Archive
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import Sidebar, { ToolCategory } from './Sidebar';
import { processImage, fetchHistogramData } from './lib/api';
import { useTheme } from './components/theme-provider';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { ResponsiveContainer, BarChart as RechartsBarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, CartesianGrid } from 'recharts';
import { useTranslation } from 'react-i18next';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

function ModeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
      className="rounded-md hover:bg-muted"
    >
      <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}

function LanguageToggle() {
  const { i18n } = useTranslation();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="rounded-md hover:bg-muted">
          <Globe className="h-4 w-4" />
          <span className="sr-only">Toggle language</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => i18n.changeLanguage('id')} className={i18n.language === 'id' ? 'font-bold' : ''}>
          Bahasa Indonesia
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => i18n.changeLanguage('en')} className={i18n.language === 'en' ? 'font-bold' : ''}>
          English
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export default function App() {
  const { t } = useTranslation();
  
  const [originalBlob, setOriginalBlob] = useState<Blob | null>(null);
  const [currentBlob, setCurrentBlob] = useState<Blob | null>(null);
  
  const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  
  const [history, setHistory] = useState<Blob[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [viewMode, setViewMode] = useState<string>('single');
  const [activeCategory, setActiveCategory] = useState<ToolCategory>(null);
  const [histogramData, setHistogramData] = useState<number[] | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (originalBlob) {
      const url = URL.createObjectURL(originalBlob);
      setOriginalUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setOriginalUrl(null);
    }
  }, [originalBlob]);

  useEffect(() => {
    if (currentBlob) {
      const url = URL.createObjectURL(currentBlob);
      setPreviewUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setPreviewUrl(null);
    }
  }, [currentBlob]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setOriginalBlob(file);
      setCurrentBlob(file);
      setHistory([]);
      setError(null);
      setActiveCategory('adjust'); 
    }
  };

  const handleApplyTool = async (endpoint: string, params: Record<string, string | number> = {}) => {
    if (!currentBlob) return;
    setIsProcessing(true);
    setError(null);
    try {
      const newBlob = await processImage(endpoint, currentBlob, params);
      setHistory(prev => [...prev, currentBlob]);
      setCurrentBlob(newBlob);
    } catch (err: any) {
      setError(err.message || "Failed to process image");
    } finally {
      setIsProcessing(false);
    }
  };

  const fetchHistogram = async () => {
    if (!currentBlob) return;
    setIsProcessing(true);
    setError(null);
    try {
      const data = await fetchHistogramData(currentBlob);
      setHistogramData(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch histogram');
    } finally {
      setIsProcessing(false);
    }
  };

  const executeAction = (action: string) => {
    if (action === 'histogram') {
      fetchHistogram();
    }
  };

  const undo = () => {
    if (history.length > 0) {
      const newHistory = [...history];
      const previousState = newHistory.pop()!;
      setHistory(newHistory);
      setCurrentBlob(previousState);
    }
  };

  const reset = () => {
    if (originalBlob) {
      setCurrentBlob(originalBlob);
      setHistory([]);
    }
  };

  const download = () => {
    if (!previewUrl) return;
    const a = document.createElement('a');
    a.href = previewUrl;
    a.download = 'photoshop-edited.jpg';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const categories = [
    { id: 'adjust', icon: SlidersHorizontal, label: t('sidebar.categories.adjust') },
    { id: 'geometry', icon: Move, label: t('sidebar.categories.geometry') },
    { id: 'color', icon: Palette, label: t('sidebar.categories.color') },
    { id: 'filters', icon: Wand2, label: t('sidebar.categories.filters') },
    { id: 'restore', icon: RefreshCw, label: t('sidebar.categories.restore') },
    { id: 'segment', icon: Layers, label: t('sidebar.categories.segment') },
    { id: 'compress', icon: Archive, label: t('sidebar.categories.compress') },
  ] as const;

  return (
    <div className="flex flex-col h-screen bg-background text-foreground overflow-hidden font-sans">
      {/* Topbar */}
      <header className="flex items-center justify-between px-4 h-14 border-b bg-background z-30 flex-shrink-0">
        <div className="flex items-center gap-3 min-w-[240px]">
          <div className="w-8 h-8 rounded-[8px] bg-primary flex items-center justify-center text-primary-foreground shadow-md">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <path d="m14.31 8 5.74 9.94"/>
              <path d="M9.69 8h11.48"/>
              <path d="m7.38 12 5.74-9.94"/>
              <path d="M9.69 16 3.95 6.06"/>
              <path d="M14.31 16H2.83"/>
              <path d="m16.62 12-5.74 9.94"/>
            </svg>
          </div>
          <span className="font-bold text-xl tracking-tight text-foreground font-heading">YOPS</span>
        </div>
        
        <div className="flex flex-1 items-center justify-center">
           {currentBlob && (
             <Tabs value={viewMode} onValueChange={setViewMode} className="w-[300px]">
                <TabsList className="grid w-full grid-cols-3 h-8">
                  <TabsTrigger value="single" className="text-xs h-6"><ImageIcon className="w-3 h-3 mr-2" />{t('app.single')}</TabsTrigger>
                  <TabsTrigger value="split" className="text-xs h-6"><SplitSquareHorizontal className="w-3 h-3 mr-2" />{t('app.split')}</TabsTrigger>
                  <TabsTrigger value="histogram" className="text-xs h-6" onClick={() => executeAction('histogram')}><BarChart className="w-3 h-3 mr-2" />{t('app.hist')}</TabsTrigger>
                </TabsList>
             </Tabs>
           )}
        </div>

        <div className="flex items-center gap-1.5 min-w-[240px] justify-end">
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileUpload} 
            accept="image/*" 
            className="hidden" 
          />
          <Button variant="outline" size="sm" onClick={() => fileInputRef.current?.click()} className="h-8 text-xs font-medium bg-background">
            <Upload className="w-3.5 h-3.5 mr-1.5" /> {t('app.open')}
          </Button>
          
          <div className="w-px h-4 bg-border/60 mx-1.5" />
          
          <TooltipProvider delayDuration={200}>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" onClick={undo} disabled={history.length === 0 || isProcessing} className="h-8 w-8 rounded-lg">
                  <Undo2 className="w-3.5 h-3.5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="bottom" className="text-xs">{t('app.undo')}</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" onClick={reset} disabled={!originalBlob || isProcessing} className="h-8 w-8 rounded-lg">
                  <RotateCcw className="w-3.5 h-3.5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="bottom" className="text-xs">{t('app.reset')}</TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <div className="w-px h-4 bg-border/60 mx-1.5" />
          
          <Button variant="default" size="sm" onClick={download} disabled={!currentBlob || isProcessing} className="h-8 text-xs font-medium rounded-lg shadow-sm">
            <Download className="w-3.5 h-3.5 mr-1.5" /> {t('app.export')}
          </Button>
          
          <div className="ml-1 flex items-center">
            <LanguageToggle />
            <ModeToggle />
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        
        {/* Left Toolbar */}
        <div className="w-16 flex-shrink-0 border-r bg-card flex flex-col items-center py-4 gap-3 z-20 shadow-sm">
          <TooltipProvider delayDuration={200}>
            {categories.map((c) => {
              const Icon = c.icon;
              const isActive = activeCategory === c.id;
              return (
                <Tooltip key={c.id}>
                  <TooltipTrigger render={
                    <Button
                      variant={isActive ? "default" : "ghost"}
                      size="icon"
                      className={`h-11 w-11 rounded-xl transition-all ${isActive ? 'shadow-sm' : 'text-muted-foreground hover:bg-muted/70'}`}
                      onClick={() => setActiveCategory(c.id as ToolCategory)}
                      disabled={!currentBlob}
                    >
                      <Icon className="w-4 h-4" />
                    </Button>
                  } />
                  <TooltipContent side="right" className="text-xs font-medium">
                    {c.label}
                  </TooltipContent>
                </Tooltip>
              );
            })}
          </TooltipProvider>
        </div>

        {/* Main Canvas Area */}
        <main className="flex-1 relative flex flex-col bg-muted/30">
          {/* Dot Grid Pattern */}
          <div className="absolute inset-0 pointer-events-none opacity-[0.03] dark:opacity-[0.05]" style={{ backgroundImage: 'radial-gradient(circle at 1.5px 1.5px, currentColor 1.5px, transparent 0)', backgroundSize: '16px 16px' }} />

          {error && (
            <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-4 py-2 rounded-md shadow-lg flex items-center gap-3 z-50">
              <AlertTriangle className="w-4 h-4" />
              <span className="text-sm font-medium">{error}</span>
              <button className="ml-2 opacity-80 hover:opacity-100 text-xs" onClick={() => setError(null)}>Close</button>
            </div>
          )}

          {!currentBlob ? (
            <div className="flex flex-col items-center justify-center w-full h-full z-10 p-8">
              <div className="flex flex-col items-center justify-center w-full max-w-lg p-12 border-2 border-dashed border-border/80 rounded-[2rem] bg-card/40 backdrop-blur-sm transition-colors hover:bg-card/60 relative group">
                <div className="absolute inset-0 bg-primary/5 rounded-[2rem] opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 text-primary shadow-sm border border-primary/20">
                  <ImageIcon className="w-8 h-8 opacity-90" strokeWidth={1.5} />
                </div>
                <h3 className="text-2xl text-foreground font-semibold tracking-tight mb-2 font-heading">{t('app.emptyState.title')}</h3>
                <p className="text-sm text-center mb-8 max-w-sm text-muted-foreground leading-relaxed">
                  {t('app.emptyState.desc')}
                </p>
                <Button size="lg" className="shadow-md rounded-xl h-11 px-8 font-medium transition-all hover:scale-[1.02]" onClick={() => fileInputRef.current?.click()}>
                  <Upload className="w-4 h-4 mr-2" /> {t('app.emptyState.btn')}
                </Button>
              </div>
            </div>
          ) : (
            <div className="relative w-full h-full flex items-center justify-center p-8 z-10 overflow-auto">
              {isProcessing && (
                <div className="absolute inset-0 bg-background/50 backdrop-blur-sm z-20 flex items-center justify-center">
                  <div className="bg-card px-4 py-3 rounded-md shadow-lg flex items-center gap-3 border">
                    <RefreshCw className="w-4 h-4 animate-spin text-primary" />
                    <span className="font-medium text-sm">{t('app.processing')}</span>
                  </div>
                </div>
              )}
              
              {viewMode === 'histogram' ? (
                <div className="w-full h-full flex flex-col items-center justify-center bg-transparent p-4">
                  <span className="text-[10px] uppercase tracking-widest text-primary mb-6 font-semibold">{t('app.histogramTitle')}</span>
                  {histogramData ? (
                    <div className="w-full max-w-4xl h-96 bg-card/50 p-6 rounded-xl border shadow-sm">
                      <ResponsiveContainer width="100%" height="100%">
                        <RechartsBarChart data={histogramData.map((val, i) => ({ intensity: i, count: val }))}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="currentColor" className="opacity-10" />
                          <XAxis dataKey="intensity" tick={{ fontSize: 10 }} tickLine={false} axisLine={false} minTickGap={30} />
                          <YAxis tick={{ fontSize: 10 }} tickLine={false} axisLine={false} tickFormatter={(v) => v >= 1000 ? `${(v/1000).toFixed(1)}k` : v} />
                          <RechartsTooltip 
                            contentStyle={{ backgroundColor: 'var(--card)', borderRadius: '8px', border: '1px solid var(--border)', fontSize: '12px' }}
                            itemStyle={{ color: 'var(--foreground)' }}
                          />
                          <Bar dataKey="count" fill="currentColor" className="text-primary" radius={[2, 2, 0, 0]} maxBarSize={4} />
                        </RechartsBarChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <div className="text-muted-foreground text-sm flex items-center">
                      <BarChart className="w-4 h-4 mr-2" /> {t('app.histogramEmpty')}
                    </div>
                  )}
                </div>
              ) : viewMode === 'single' ? (
                <div className="relative max-w-full max-h-full flex items-center justify-center bg-transparent drop-shadow-xl">
                  <img 
                    src={previewUrl!} 
                    alt="Canvas" 
                    className="max-w-full max-h-[calc(100vh-8rem)] object-contain transition-opacity duration-200 shadow-xl ring-1 ring-border/50" 
                    style={{ opacity: isProcessing ? 0.3 : 1 }}
                  />
                </div>
              ) : (
                <div className="w-full h-full flex flex-col md:flex-row items-center gap-8 p-4">
                  <div className="flex-1 flex flex-col items-center justify-center w-full h-full min-h-0">
                    <span className="text-[10px] uppercase tracking-widest text-muted-foreground mb-3 font-semibold">{t('app.original')}</span>
                    <div className="relative flex items-center justify-center flex-1 w-full drop-shadow-lg">
                      <img 
                        src={originalUrl!} 
                        alt="Original" 
                        className="max-w-full max-h-[calc(100vh-10rem)] object-contain ring-1 ring-border/50 shadow-xl" 
                      />
                    </div>
                  </div>
                  
                  <div className="flex-1 flex flex-col items-center justify-center w-full h-full min-h-0">
                    <span className="text-[10px] uppercase tracking-widest text-primary mb-3 font-semibold">{t('app.modified')}</span>
                    <div className="relative flex items-center justify-center flex-1 w-full drop-shadow-lg">
                      <img 
                        src={previewUrl!} 
                        alt="Modified" 
                        className="max-w-full max-h-[calc(100vh-10rem)] object-contain transition-opacity duration-200 ring-1 ring-border/50 shadow-xl"
                        style={{ opacity: isProcessing ? 0.3 : 1 }}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </main>
        
        {/* Properties Panel (Right Sidebar) */}
        <Sidebar 
          activeCategory={activeCategory}
          onApplyTool={handleApplyTool} 
          isProcessing={isProcessing} 
          disabled={!currentBlob} 
        />
      </div>
    </div>
  );
}
